from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import ModelViewSet

from src.blog.models import PostCategory, Post, PostTag
from src.blog.permissions import (
    PostCategoryPermission,
    PostTagPermission,
    BlogPostPermission,
)

from .serializers import (
    PostCategoryCreateSerializer,
    PostCategoryListSerializer,
    PostCategoryDetailSerializer,
    PostCategoryUpdateSerializer,
    PostTagCreateSerializer,
    PostTagDetailSerializer,
    PostTagListSerializer,
    PostTagUpdateSerializer,
    PostCreateSerializer,
    PostDetailSerializer,
    PostListSerializer,
    PostUpdateSerializer
)
from .filters import FilterForPostCategoryViewSet, FilterForPostTagViewSet, FilterForPostViewSet


class PostCategoryViewSet(ModelViewSet):
    """
    Retrieve, create, update, or list blog categories.
    This API supports filtering, searching, and ordering of categories.
    """

    permission_classes = [PostCategoryPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = FilterForPostCategoryViewSet
    search_fields = ["name", "slug", "description"]
    ordering = ["-created_at"]
    ordering_fields = ["name", "created_at"]
    http_method_names = ["options", "head", "get", "post", "patch"]

    def get_queryset(self):
        if self.action == "list":
            return PostCategory.objects.filter(is_archived=False, parent__isnull=True)
        return PostCategory.objects.filter(is_archived=False)

    def get_serializer_class(self):
        serializer_class = PostCategoryListSerializer
        if self.request.method == "GET":
            if self.action == "list":
                serializer_class = PostCategoryListSerializer
            else:
                serializer_class = PostCategoryDetailSerializer
        if self.request.method == "POST":
            serializer_class = PostCategoryCreateSerializer
        if self.request.method == "PATCH":
            serializer_class = PostCategoryUpdateSerializer

        return serializer_class


class PostTagViewSet(ModelViewSet):
    """
    Retrieve, create, update, or list blog tags.
    This API supports filtering, searching, and ordering of tags.
    """

    permission_classes = [PostTagPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = FilterForPostTagViewSet
    search_fields = ["name", "slug", "description"]
    ordering = ["-created_at"]
    ordering_fields = ["created_at"]
    http_method_names = ["options", "head", "get", "post", "patch"]

    def get_queryset(self):
        return PostTag.objects.filter(is_archived=False)

    def get_serializer_class(self):
        serializer_class = PostTagListSerializer
        if self.request.method == "GET":
            if self.action == "list":
                serializer_class = PostTagListSerializer
            else:
                serializer_class = PostTagDetailSerializer
        if self.request.method == "POST":
            serializer_class = PostTagCreateSerializer
        if self.request.method == "PATCH":
            serializer_class = PostTagUpdateSerializer

        return serializer_class


class PostViewSet(ModelViewSet):
    """
    Retrieve, create, update, or list blog posts.
    This API supports filtering, searching, and ordering of posts.
    """

    permission_classes = [BlogPostPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = FilterForPostViewSet
    search_fields = ["title", "slug"]
    ordering = ["-created_at"]
    ordering_fields = ["created_at", "published_at"]
    http_method_names = ["options", "head", "get", "post", "patch"]

    def get_queryset(self):
        return Post.objects.filter(is_archived=False)

    def get_serializer_class(self):
        serializer_class = PostListSerializer
        if self.request.method == "GET":
            if self.action == "list":
                serializer_class = PostListSerializer
            else:
                serializer_class = PostDetailSerializer
        if self.request.method == "POST":
            serializer_class = PostCreateSerializer
        if self.request.method == "PATCH":
            serializer_class = PostUpdateSerializer

        return serializer_class
