from django_filters.filterset import FilterSet
from .models import PostTag, PostCategory, Post


class FilterForPostCategoryViewSet(FilterSet):
    """Filters for Blog Post Category"""

    class Meta:
        model = PostCategory
        fields = ["name", "is_active", "parent"]


class FilterForPostTagViewSet(FilterSet):
    """Filters for Blog Post Tag"""

    class Meta:
        model = PostTag
        fields = ["name", "is_active"]


class FilterForPostViewSet(FilterSet):
    """Filters for Blog Post"""

    class Meta:
        model = Post
        fields = ["title", "is_active"]
