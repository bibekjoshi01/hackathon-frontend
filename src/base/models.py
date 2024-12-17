import uuid
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class AbstractInfoModel(models.Model):
    """Abstract Created Info Model"""

    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(
        _("created date"),
        default=timezone.now,
        editable=False,
    )
    updated_at = models.DateTimeField(_("date updated"), auto_now=True)
    created_by = models.ForeignKey("user.User", on_delete=models.PROTECT)
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this object should be treated as active. "
            "Unselect this instead of deleting instances.",
        ),
    )
    is_archived = models.BooleanField(
        _("archived"),
        default=False,
        help_text=_(
            "Designates whether this object should be treated as delected. "
            "Unselect this instead of deleting instances.",
        ),
    )

    class Meta:
        abstract = True

    @staticmethod
    def get_upload_path(upload_path: str, filename: str) -> str:
        return f"{upload_path}/{filename}"


class PublicAbstractInfoModel(models.Model):
    
    """Abstract Created Info Model For Public Models"""
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(
        _("created date"),
        default=timezone.now,
        editable=False,
    )
    updated_at = models.DateTimeField(_("date updated"), auto_now=True)
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this object should be treated as active. "
            "Unselect this instead of deleting instances.",
        ),
    )
    is_archived = models.BooleanField(
        _("archived"),
        default=False,
        help_text=_(
            "Designates whether this object should be treated as deleted. "
            "Unselect this instead of deleting instances.",
        ),
    )

    class Meta:
        abstract = True

    @staticmethod
    def get_upload_path(upload_path: str, filename: str) -> str:
        return f"{upload_path}/{filename}"
