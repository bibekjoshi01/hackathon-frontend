from rest_framework.permissions import BasePermission

from src.libs.permissions import validate_permissions


class PostCategoryPermission(BasePermission):
    def has_permission(self, request, view):
        user_permissions_dict = {
            "SAFE_METHODS": "view_post_category",
            "POST": "add_post_category",
            "PATCH": "edit_post_category",
            "DELETE": "delete_post_category",
        }

        return validate_permissions(request, user_permissions_dict)


class PostTagPermission(BasePermission):
    def has_permission(self, request, view):
        user_permissions_dict = {
            "SAFE_METHODS": "view_post_tag",
            "POST": "add_post_tag",
            "PATCH": "edit_post_tag",
            "DELETE": "delete_post_tag",
        }

        return validate_permissions(request, user_permissions_dict)


class BlogPostPermission(BasePermission):
    def has_permission(self, request, view):
        user_permissions_dict = {
            "SAFE_METHODS": "view_blog_post",
            "POST": "add_blog_post",
            "PATCH": "edit_blog_post",
            "DELETE": "delete_blog_post",
        }

        return validate_permissions(request, user_permissions_dict)


class BlogCommentPermission(BasePermission):
    def has_permission(self, request, view):
        user_permissions_dict = {
            "SAFE_METHODS": "view_blog_comment",
            "POST": "add_blog_comment",
            "PATCH": "edit_blog_comment",
            "DELETE": "delete_blog_comment",
        }

        return validate_permissions(request, user_permissions_dict)
