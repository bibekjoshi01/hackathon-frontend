# Standard Library Imports
from uuid import uuid4

# Django Imports
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

# Third Party Apps Imports
from mptt.managers import TreeManager
from mptt.models import TreeForeignKey, MPTTModel

# Custom Imports
from .validators import validate_blog_media
from src.base.models import AbstractInfoModel
from .constants import CommentStatus, PostStatus, PostFormat, PostVisibility

User = get_user_model()


class Post(AbstractInfoModel):
    """
    Represents a post for a blog.
    """
    id: int
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    title = models.CharField(
        _("Title"),
        max_length=255,
        help_text=_("Title of the post."),
    )
    cover_image = models.ImageField(null=True, help_text=_(
        "Cover image of blog post, Use a ratio of 4:3 for best results."
    ))
    slug = models.SlugField(
        unique=True,
        max_length=255,
        help_text=_(
            "URL-friendly version of the title. Lowercase with letters, numbers, and hyphens."
        ),
    )
    status = models.CharField(
        choices=PostStatus.choices(),
        max_length=20,
        default="PUBLISHED",
        help_text=_("Publication status of the post."),
    )
    format = models.CharField(
        choices=PostFormat.choices(),
        max_length=15,
        help_text=_(
            "Post format which designates how the theme will display the post."
        ),
    )
    visibility = models.CharField(
        choices=PostVisibility.choices(),
        max_length=20,
        help_text=_(
            "Determines who can see this post. "
            "Public posts are visible to everyone, "
            "private posts are only visible to the author, "
            "and password-protected posts require a password to access."
        ),
    )
    content = models.TextField(
        help_text=_("Main content of the post."),
    )
    excerpt = models.CharField(
        _("Excerpt"),
        max_length=255,
        blank=True,
        help_text=_("Short description of the post, used in summaries and thumbnails."),
    )
    author = models.ForeignKey(
        User,
        verbose_name=_("Post Author"),
        on_delete=models.PROTECT,
        related_name="user_posts",
        help_text=_("Author of the post."),
    )
    read_time = models.PositiveSmallIntegerField(
        default=0,
        help_text=_("Estimated reading time in minutes."),
    )
    categories = models.ManyToManyField(
        "blog.PostCategory",
        related_name="posts",
        help_text=_("Categories this post belongs to."),
    )
    tags = models.ManyToManyField(
        "blog.PostTag",
        related_name="posts",
        help_text=_("Tags associated with this post."),
    )
    stick_at_top = models.BooleanField(
        _("Stick at Top"),
        default=False,
        help_text=_("Stick this post to the top of the blog page."),
    )
    published_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("Publication date of the post."),
    )
    allow_comments = models.BooleanField(_("Allow Comments"), default=True)
    views = models.PositiveIntegerField(_("views"), default=0)
    up_votes = models.PositiveIntegerField(_("up votes"), default=0)
    down_votes = models.PositiveIntegerField(_("down votes"), default=0)

    class Meta:
        ordering = ["-published_at"]
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["slug"]),
            models.Index(fields=["status"]),
            models.Index(fields=["published_at"]),
        ]

    def __str__(self) -> str:
        return self.title

    @property
    def get_author_full_name(self) -> str:
        return self.author.get_full_name

    def set_viewed(self) -> None:
        self.views += 1
        self.save(update_fields=["views"])

    def get_unread_comments(self) -> int:
        return self.comments.filter(is_seen=False, is_archived=False).count()

    def get_total_comments(self) -> int:
        return self.comments.filter(is_archived=False).count()

    def get_next_post(self):
        return (
            Post.objects.filter(id__gt=self.id, status=PostStatus.PUBLISHED.value)
            .order_by("id")
            .first()
        )

    def get_prev_post(self):
        return Post.objects.filter(id__lt=self.id, status=PostStatus.PUBLISHED.value).first()


class PostCategory(MPTTModel, AbstractInfoModel):
    """
    Represents a category for organizing blog posts.
    Categories can be nested to form a hierarchy.
    """
    id: int
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    name = models.CharField(
        _("name"),
        max_length=50,
        unique=True,
        help_text=_("The name as it appears on your site."),
    )
    slug = models.SlugField(
        max_length=55,
        unique=True,
        help_text=_(
            "URL-friendly version of the name. Lowercase with letters, numbers, and hyphens."
        ),
    )
    description = models.TextField(
        help_text=_("Optional description; may be displayed by some themes."),
        blank=True,
    )
    parent = TreeForeignKey(
        "self",
        null=True,
        blank=True,
        verbose_name=_("Parent Category"),
        related_name="sub_categories",
        on_delete=models.CASCADE,
        help_text=_("Categories can have a hierarchy. Totally optional."),
    )

    objects = models.Manager()
    tree = TreeManager()  # type: ignore[django-manager-missing]

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["slug"]),
        ]

    def get_post_count(self) -> int:
        """
        Returns the count of posts associated with this category.
        Cached for 10 hours.
        """
        return Post.objects.filter(categories__name=self.name).distinct().count()

    def __str__(self) -> str:
        return self.name


class PostTag(AbstractInfoModel):
    """
    Represents a tag for labeling blog posts.
    Tags are non-hierarchical keywords.
    """
    id: int
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    name = models.CharField(
        _("Tag Name"),
        max_length=50,
        unique=True,
        help_text=_("The name as it appears on your site."),
    )
    slug = models.SlugField(
        max_length=55,
        unique=True,
        help_text=_(
            "URL-friendly version of the name. Lowercase with letters, numbers, and hyphens."
        ),
    )
    description = models.TextField(
        help_text=_("Optional description; may be displayed by some themes."),
        blank=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["slug"]),
        ]

    def get_post_count(self):
        """
        Returns the count of posts associated with this tag.
        Cached for 10 hours.
        """
        return Post.objects.filter(tags__name=self.name).distinct().count()

    def __str__(self) -> str:
        return self.name


class PostComment(MPTTModel, AbstractInfoModel):
    """
    Represents a multilevel comment model for a blog post.
    Comments can have a hierarchy, allowing replies to comments.
    """

    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    user = models.ForeignKey(
        User,
        verbose_name=_("Author"),
        null=True,
        on_delete=models.PROTECT,
        related_name="user_comments",
        help_text=_("The user who made the comment. Null if the comment is anonymous."),
    )
    parent = TreeForeignKey(
        "self",
        null=True,
        blank=True,
        verbose_name=_("Parent Comment"),
        related_name="replies",
        on_delete=models.CASCADE,
        help_text=_("Parent comment if this comment is a reply. Totally optional."),
    )

    objects = models.Manager()
    tree = TreeManager()  # type: ignore[django-manager-missing]

    full_name = models.CharField(
        _("Full Name"),
        max_length=50,
        blank=True,
        help_text=_("Required if the comment is made by an anonymous user."),
    )
    email = models.EmailField(
        _("Email"),
        max_length=254,
        blank=True,
        help_text=_("Required if the comment is made by an anonymous user."),
    )
    post = models.ForeignKey(
        "Post",
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("Post"),
        help_text=_("The blog post this comment is related to."),
    )
    message = models.TextField(
        _("Message"),
        max_length=500,
        help_text=_("The content of the comment."),
    )
    status = models.CharField(
        _("Status"),
        max_length=30,
        choices=CommentStatus.choices(),
        blank=True,
        default="APPROVED",
        help_text=_("The status of the comment (e.g., approved, moderation)."),
    )
    is_edited = models.BooleanField(
        _("Is Edited"),
        default=False,
        help_text=_("Indicates if the comment has been edited."),
    )
    is_seen = models.BooleanField(
        _("Is seen"), default=False, help_text="Is comment seen by admin."
    )
    seen_by = models.ForeignKey(
        User,
        verbose_name=_("seen by"),
        null=True,
        on_delete=models.PROTECT,
        related_name="user_seen_comments",
        help_text=_("The admin user who mark the comment seen."),
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Post Comment")
        verbose_name_plural = _("Post Comments")
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["post"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"Comment by {self.user or self.full_name} on {self.post}"


class BlogMedia(models.Model):
    """Blog Media Model"""

    id: int
    file = models.FileField(
        upload_to="blog/blog_media",
        validators=[validate_blog_media],
        help_text="Media max size: 2MB",
    )

    def __str__(self):
        return str(self.id)
