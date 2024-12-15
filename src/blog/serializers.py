from typing import List, Dict, Union, Any
from drf_spectacular.utils import extend_schema_field

from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth import get_user_model

from src.base.serializers import AbstractInfoRetrieveSerializer
from src.blog.constants import PostStatus
from src.blog.messages import CATEGORY_NAME_EXISTS, CATEGORY_CREATED_SUCCESS, CATEGORY_UPDATED_SUCCESS, \
    POST_SLUG_EXISTS, POST_UPDATED_SUCCESS, POST_CREATED_SUCCESS, TAG_CREATED_SUCCESS, TAG_NAME_EXISTS, \
    TAG_UPDATED_SUCCESS
from src.blog.schemas import sub_category_schema
from src.libs.get_context import get_user_by_context
from src.blog.models import PostCategory, PostTag, Post

User = get_user_model()


# Blog Post Category Serializers


class PostCategoryListSerializer(serializers.ModelSerializer):
    post_count = serializers.IntegerField(source="get_post_count")
    sub_categories = serializers.SerializerMethodField()

    class Meta:
        model = PostCategory
        fields = ["id", "name", "description", "slug", "post_count", "sub_categories"]

    @extend_schema_field(sub_category_schema)
    def get_sub_categories(self, obj: PostCategory) -> List[Dict]:
        if obj.is_leaf_node():
            return []
        serializer = self.__class__(obj.get_children(), many=True)
        return serializer.data


class PostCategoryDetailSerializer(AbstractInfoRetrieveSerializer):
    post_count = serializers.IntegerField(source="get_post_count")

    class Meta(AbstractInfoRetrieveSerializer.Meta):
        model = PostCategory
        fields = ["id", "name", "description", "parent", "slug", "post_count"]

        fields += AbstractInfoRetrieveSerializer.Meta.fields


class PostCategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCategory
        fields = ["name", "slug", "description", "parent"]

    def validate_name(self, name: str) -> str:
        """Validate the uniqueness of the category name."""
        if PostCategory.objects.filter(name=name).exists():
            raise serializers.ValidationError(CATEGORY_NAME_EXISTS.format(name=name))
        return name

    def create(self, validated_data):
        created_by = get_user_by_context(self.context)

        return PostCategory.objects.create(
            created_by=created_by,
            **validated_data,
        )

    def to_representation(self, instance: PostCategory) -> Dict[str, Union[str, int]]:
        data = super(PostCategoryCreateSerializer, self).to_representation(instance)
        data["type"] = "success"
        data["message"] = CATEGORY_CREATED_SUCCESS
        data["id"] = instance.id
        return data


class PostCategoryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCategory
        fields = ["name", "slug", "description", "parent", "is_active"]

    def update(self, instance: PostCategory, validated_data: Dict) -> PostCategory:
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance

    def to_representation(self, instance: PostCategory) -> Dict:
        return {
            "type": "success",
            "message": CATEGORY_UPDATED_SUCCESS,
            "id": instance.id,
        }


# Blog Post Tag Serializers


class PostTagListSerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()

    class Meta:
        model = PostTag
        fields = ["id", "name", "description", "slug", "post_count"]

    def get_post_count(self, obj: PostTag) -> int:
        return obj.get_post_count()


class PostTagDetailSerializer(AbstractInfoRetrieveSerializer):
    post_count = serializers.SerializerMethodField()

    class Meta(AbstractInfoRetrieveSerializer.Meta):
        model = PostTag
        fields = ["id", "name", "description", "slug", "post_count"]

        fields += AbstractInfoRetrieveSerializer.Meta.fields

    def get_post_count(self, obj: PostTag) -> int:
        return obj.get_post_count()


class PostTagCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostTag
        fields = ["name", "slug", "description"]

    def validate_name(self, name):
        """
        Validate that the name is unique.
        """
        if PostTag.objects.filter(name=name).exists():
            raise serializers.ValidationError(TAG_NAME_EXISTS.format(name=name))
        return name

    def create(self, validated_data):
        created_by = get_user_by_context(self.context)

        return PostTag.objects.create(
            created_by=created_by,
            **validated_data,
        )

    def to_representation(self, instance: PostTag) -> Dict[str, Union[str, int]]:
        return {
            "type": "success",
            "message": TAG_CREATED_SUCCESS,
            "id": instance.id,
        }


class PostTagUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostTag
        fields = ["name", "description", "is_active"]

    def update(self, instance: PostTag, validated_data: Dict[str, Union[str, int]]):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance

    def to_representation(self, instance: PostTag) -> dict[str, Union[str, int]]:
        return {
            "type": "success",
            "message": TAG_UPDATED_SUCCESS,
            "id": instance.id,
        }


# Blog Post Serializers


class PostListSerializer(serializers.ModelSerializer):
    total_comments = serializers.SerializerMethodField()
    unread_comments = serializers.SerializerMethodField()
    author_full_name = serializers.ReadOnlyField(source="get_author_full_name")

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "slug",
            "categories",
            "tags",
            "author_full_name",
            "unread_comments",
            "total_comments",
        ]

    def to_representation(self, instance: Post) -> Dict[str, Union[int, str]]:
        data = super().to_representation(instance)

        if instance.status == PostStatus.PUBLISHED.value:
            data["published_at"] = instance.published_at
        else:
            data["updated_at"] = instance.updated_at

        return data


class CategorySerializerForPostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCategory
        fields = ["id", "name"]


class TagSerializerForPostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostTag
        fields = ["id", "name"]


class PostDetailSerializer(serializers.ModelSerializer):
    author_full_name = serializers.ReadOnlyField(source="get_author_full_name")
    categories = CategorySerializerForPostDetailSerializer(many=True)
    tags = TagSerializerForPostDetailSerializer(many=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "slug",
            "status",
            "views",
            "up_votes",
            "down_votes",
            "categories",
            "tags",
            "published_at",
            "author_full_name",
        ]

    def to_representation(self, instance: Post) -> dict[str, Union[str, int]]:
        data = super().to_representation(instance)

        if instance.status == "PUBLISHED":
            data["published_at"] = instance.published_at
        else:
            data["updated_at"] = instance.updated_at

        return data


class PostCreateSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_archived=False, is_active=True)
    )
    categories = serializers.PrimaryKeyRelatedField(
        queryset=PostCategory.objects.filter(is_archived=False, is_active=True),
        many=True,
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=PostTag.objects.filter(is_archived=False, is_active=True), many=True
    )

    class Meta:
        model = Post
        fields = [
            "title",
            "slug",
            "status",
            "format",
            "visibility",
            "content",
            "excerpt",
            "author",
            "read_time",
            "categories",
            "tags",
            "stick_at_top",
            "allow_comments",
        ]

    def validate_slug(self, slug: str) -> str:
        if Post.objects.filter(slug=slug).exists():
            raise serializers.ValidationError(POST_SLUG_EXISTS.format(slug=slug))
        return slug

    def create(self, validated_data: Dict[str, Any]) -> Post:
        created_by = get_user_by_context(self.context)

        # Extracting nested data
        categories = validated_data.pop("categories", [])
        tags = validated_data.pop("tags", [])

        # Set the publication timestamp if the post status is PUBLISHED
        if validated_data["status"] == PostStatus.PUBLISHED.value:
            validated_data["published_at"] = timezone.now()

        # Create the post instance
        post = Post.objects.create(
            title=validated_data.pop("title").title(),
            slug=validated_data.pop("slug"),
            created_by=created_by,
            **validated_data,
        )

        # Add categories and tags
        post.categories.add(*categories)
        post.tags.add(*tags)

        return post

    def to_representation(self, instance: Post) -> Dict[str, Union[str, int]]:
        return {
            "type": "success",
            "message": POST_CREATED_SUCCESS,
            "id": instance.id,
        }


class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["title", "content", "is_active"]

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance

    def to_representation(self, instance: Post) -> dict[str, Union[str, int]]:
        return {
            "type": "success",
            "message": POST_UPDATED_SUCCESS,
            "id": instance.id,
        }
