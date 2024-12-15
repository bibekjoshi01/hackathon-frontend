# Standard Library Imports
from uuid import uuid4

# Django Core Imports
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager

# Third-Party Package Imports
from rest_framework_simplejwt.tokens import RefreshToken

# Custom Imports
from src.base.models import AbstractInfoModel
from src.user.exceptions import (
    EmailNotSetError,
    IsStaffError,
    IsSuperuserError,
    UserRoleNotFound,
)
from .validators import CustomUsernameValidator, validate_image
from .oauth.constants import AuthProviders


class PermissionCategory(AbstractInfoModel):
    """Permission Category to group permissions"""

    id: int
    name = models.CharField(max_length=100)
    codename = models.CharField(_("codename"), unique=True, max_length=100)

    def __str__(self) -> str:
        return f"id - {self.id} : {self.name}"


class UserPermission(AbstractInfoModel):
    """
    The permissions system provides a way to assign permissions to specific
    users and groups of users.
    """

    name = models.CharField(_("name"), max_length=100)
    codename = models.CharField(_("codename"), unique=True, max_length=100)
    permission_category = models.ForeignKey(
        PermissionCategory, on_delete=models.PROTECT, related_name="permissions"
    )

    class Meta:
        verbose_name = _("permission")
        verbose_name_plural = _("permissions")
        ordering = ["permission_category", "id"]

    def __str__(self) -> str:
        return f"{self.permission_category} : {self.name}"


class UserRole(AbstractInfoModel):
    """
    Roles are a generic way of categorizing users to apply permissions, or
    some other label, to those users. A user can belong to any number of
    roles.
    """

    name = models.CharField(_("name"), max_length=50, unique=True)
    codename = models.CharField(_("codename"), max_length=50, unique=True)
    permissions = models.ManyToManyField(
        UserPermission,
        verbose_name=_("permissions"),
        blank=True,
    )
    is_system_managed = models.BooleanField(_("System Managed"), default=False)

    class Meta:
        verbose_name = _("user role")
        verbose_name_plural = _("user roles")

    def __str__(self) -> str:
        return self.name


class UserManager(BaseUserManager):
    use_in_migrations = False

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise EmailNotSetError
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_system_user(self, username, email, password, **extra_fields):
        user = self.create_user(username, email, password, **extra_fields)
        try:
            user_group = UserRole.objects.get(codename="SYSTEM-VENDOR")
            user.groups.add(user_group)
        except UserRole.DoesNotExist as err:
            user_group = "System User"
            raise UserRoleNotFound(user_group) from err
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise IsStaffError

        if extra_fields.get("is_superuser") is not True:
            raise IsSuperuserError

        user = self._create_user(username, email, password, **extra_fields)
        try:
            user_group = UserRole.objects.get(codename="SYSTEM-VENDOR")
            user.groups.add(user_group)
        except UserRole.DoesNotExist as err:
            pass
            # user_group = "System Vendor"
            # raise UserRoleNotFound(user_group) from err
        user.save()
        return user

    def create_public_user(self, username, email=None, password=None, **extra_fields):
        user = self._create_user(username, email, password, **extra_fields)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User Model"""

    uuid = models.UUIDField(default=uuid4, unique=True, editable=False)

    username_validator = CustomUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=30,
        unique=True,
        help_text=_(
            "Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.",
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_("first name"), max_length=100, blank=True)
    middle_name = models.CharField(_("middle Name"), max_length=100, blank=True)
    last_name = models.CharField(_("last name"), max_length=100, blank=True)
    email = models.EmailField(_("email address"), unique=True, blank=True)
    phone_no = models.CharField(_("phone number"), max_length=15, blank=True)
    bio = models.TextField(blank=True)  
    photo = models.ImageField(
        validators=[validate_image],
        blank=True,
        null=True,
        default="",
    )
    is_superuser = models.BooleanField(
        _("superuser status"),
        default=False,
        help_text=_(
            "Designates that this user has all permissions without "
            "explicitly assigning them.",
        ),
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Select this for deactivating accounts.",
        ),
    )
    is_archived = models.BooleanField(
        _("archived"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as deleted. "
            "Unselect this instead of deleting users.",
        ),
    )
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    auth_provider = models.CharField(
        max_length=30,
        blank=True,
        default="BY-CREDENTIALS",
        choices=AuthProviders.choices(),
    )
    groups = models.ManyToManyField(
        UserRole,
        verbose_name=_("user groups"),
        blank=True,
        help_text=_(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups.",
        ),
        related_name="user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        UserPermission,
        verbose_name=_("user permissions"),
        blank=True,
        help_text=_("Specific permissions for this user."),
        related_name="user_set",
        related_query_name="user",
    )

    date_joined = models.DateTimeField(
        _("date joined"), default=timezone.now, editable=False
    )
    updated_at = models.DateTimeField(_("date updated"), auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
    )
    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        ordering = ["-id"]
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def __str__(self) -> str:
        return str(self.email)

    def get_upload_path(self, upload_path: str, filename: str) -> str:
        return f"{upload_path}/{filename}"

    @property
    def full_name(self) -> str:
        """
        Return the first_name plus the last_name, with a space in between.
        """
        if self.middle_name and self.first_name and self.last_name:
            full_name = f"{self.first_name} {self.middle_name} {self.last_name}"
        elif self.first_name and self.last_name:
            full_name = f"{self.first_name} {self.last_name}"
        else:
            full_name = ""
        return full_name.strip()

    def is_public_user(self):
        return self.groups.filter(codename="PUBLIC-USER").exists()

    @property
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}


class UserAccountVerification(models.Model):
    """User Account Verification"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=256)
    created_at = models.DateTimeField()
    is_archived = models.BooleanField(default=False)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"User Id: {self.user.id!s} + '-' + {self.token}"
