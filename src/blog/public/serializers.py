# Django Imports
from django.contrib.auth import get_user_model

# Rest Framework Imports
from rest_framework import serializers
from slugify import slugify

# Custom Imports
from ..constants import PostStatus
from ..models import Post, PostCategory
from src.core.constants import MAX_PUBLIC_POST_TAG_LIMIT, MAX_PUBLIC_POST_CATEGORY_LIMIT

User = get_user_model()


class AuthorForPublicPostSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="full_name")

    class Meta:
        model = User
        fields = ["uuid", "full_name"]


class PublicPostsListSerializer(serializers.ModelSerializer):
    author = AuthorForPublicPostSerializer()
    total_comments = serializers.IntegerField(source="get_total_comments()")

    class Meta:
        model = Post
        fields = [
            "uuid",
            "title",
            "cover_image",
            "slug",
            "format",
            "excerpt",
            "read_time",
            "published_at",
            "views",
            "author",
            "total_comments"
        ]


class PublicPostCreateSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(
        child=serializers.CharField(),
        max_length=MAX_PUBLIC_POST_TAG_LIMIT
    )
    categories = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(
            queryset=PostCategory.objects.filter(is_active=True)
        ), max_length=MAX_PUBLIC_POST_CATEGORY_LIMIT
    )
    status = serializers.ChoiceField(choices=PostStatus.public_choices())

    class Meta:
        model = Post
        fields = [
            "title",
            "tags",
            "content",
            "cover_image",
            "status",
            "format",
            "visibility",
            "read_time",
            "categories",
            "allow_comments",
        ]

    def create(self, validated_data) -> Post:
        validated_data["slug"] = slugify(validated_data["title"])
        tags = validated_data.pop("tags", [])
        categories = validated_data.pop("categories", [])

        post = Post.objects.create(**validated_data)

        if tags:
            post.tags.add(*tags)

        if categories:
            post.categories.add(*categories)

        post.save()
        return post

    def to_representation(self, instance) -> dict[str, str]:
        return {"message": "Post Created Successfully!"}


