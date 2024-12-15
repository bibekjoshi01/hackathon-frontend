from elasticsearch_dsl import Q
from django_filters.filterset import FilterSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from src.product.recommendation.algorithm import get_product_recommendations
from src.product.recommendation.function import calculate_demand_scores
from .utils import generate_product_description


class ProductDescriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_name = request.data.get("product_name")
        category = request.data.get("category")
        additional_info = request.data.get("additional_info", "")

        if not product_name or not category:
            return Response(
                {"error": "Product name and category are required."}, status=400
            )

        try:
            description = generate_product_description(
                product_name, category, additional_info
            )
            return Response({"description": description}, status=200)
        except ValueError as e:
            return Response({"error": str(e)}, status=500)


from src.product.models import Product, ProductCategory
from src.product.serializers import (
    ProductCategorySerializer,
    ProductCreateSerializer,
    ProductListSerializer,
    ProductRetrieveSerializer,
    ProductUpdateSerializer,
)


class FilterForProductViewSet(FilterSet):
    """Filters for Product ViewSet"""

    class Meta:
        model = Product
        fields = ["is_active", "category"]


class ProductViewSet(ModelViewSet):
    """Product ViewSet"""

    permission_classes = [IsAuthenticated]
    queryset = Product.objects.filter(is_archived=False)
    serializer_class = ProductListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = FilterForProductViewSet
    search_fields = ["name"]
    ordering = ["-created_at"]
    ordering_fields = ["id", "created_at"]
    http_method_names = ["options", "head", "get", "post", "patch"]

    def get_queryset(self):
        return self.queryset.filter(farmer=self.request.user)

    def get_serializer_class(self):
        serializer_class = ProductListSerializer
        if self.request.method == "GET":
            if self.action == "list":
                serializer_class = ProductListSerializer
            else:
                serializer_class = ProductRetrieveSerializer
        if self.request.method == "POST":
            serializer_class = ProductCreateSerializer
        if self.request.method == "PATCH":
            serializer_class = ProductUpdateSerializer

        return serializer_class


class ProductCategoryListAPIView(ListAPIView):
    queryset = ProductCategory.objects.filter(is_active=True)
    serializer_class = ProductCategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering = ["name"]
    search_fields = ["name"]
    ordering_fields = ["name"]


class ProductDescriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_name = request.data.get("product_name")
        category = request.data.get("category")
        additional_info = request.data.get("additional_info", "")

        if not product_name or not category:
            return Response(
                {"error": "Product name and category are required."}, status=400
            )

        try:
            description = generate_product_description(
                product_name, category, additional_info
            )
            return Response({"description": description}, status=200)
        except ValueError as e:
            return Response({"error": str(e)}, status=500)


class ProductRecommendationAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        demand_scores = calculate_demand_scores()

        # Fetch product details
        product_ids = [item["product_id"] for item in demand_scores]
        products = Product.objects.filter(id__in=product_ids)
        product_data = [
            {
                "id": product.id,
                "name": product.name,
                "demand_score": next(
                    item["demand_score"]
                    for item in demand_scores
                    if item["product_id"] == product.id
                ),
            }
            for product in products
        ]

        return Response({"top_demanding_products": product_data})
