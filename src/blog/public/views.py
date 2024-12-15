from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import PublicPostsListSerializer, PublicPostCreateSerializer
from ..models import Post


class PublicPostsListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = PublicPostsListSerializer
    queryset = Post.objects.filter(status="PUBLISHED")


class PublicPostCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PublicPostCreateSerializer

