from django.urls import path
from rest_framework import routers

from .views import PostViewSet, PostCategoryViewSet, PostTagViewSet

router = routers.DefaultRouter(trailing_slash=False)

router.register("categories", PostCategoryViewSet, basename="blog_post_category")
router.register("tags", PostTagViewSet, basename="blog_post_tag")
router.register("posts", PostViewSet, basename="blog_post")

# listing apis
list_urls = [
]

urlpatterns = [*list_urls, *router.urls]
