from rest_framework import serializers

from src.blog.models import PostCategory


class PostCategoryListSerializer(serializers.ModelSerializer):
    sub_categories = serializers.SerializerMethodField()

    class Meta:
        model = PostCategory
        fields = ["id", "name", "sub_categories"]

    def get_sub_categories(self, obj):
        if obj.is_leaf_node():
            return None
        serializer = self.__class__(obj.get_children(), many=True)
        return serializer.data
