from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from django_filters.filterset import FilterSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


from src.product.models import Product, ProductCategory, ProductClick, ProductReview, ProductSearch
from .serializers import (
    ProductReviewCreateSerializer,
    PublicProductListSerializer,
    ProductCategorySerializer,
    PublicProductRetrieveSerializer,
)


class PublicCategoryListAPIView(ListAPIView):
    queryset = ProductCategory.objects.filter(is_active=True)
    serializer_class = ProductCategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering = ["name"]
    search_fields = ["name"]
    ordering_fields = ["name"]


class PublicProductListAPIView(ListAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = PublicProductListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["price", "category", "farmer"]
    search_fields = ["name", "description"]
    ordering = ["-name", "price"]
    ordering_fields = ["id", "price"]

    def get(self, request, *args, **kwargs):
        # Capture the search query from the request
        search_query = request.query_params.get("search", None)
        
        # Save the search query if it exists
        if search_query:
            ProductSearch.objects.create(query=search_query)
        
        # Proceed with the normal GET logic
        return super().get(request, *args, **kwargs)
    

class PublicProductRetrieveAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = PublicProductRetrieveSerializer
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        try:
            product = self.get_object()
            ProductClick.objects.create(product=product)
            serializer = self.get_serializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND
            )
    

class ProductReviewCreateAPIView(CreateAPIView):
    """
    API to create a review for a product.
    Ensures valid rating and saves the review.
    """
    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(created_by=user)


# class SearchProductInventory(APIView, LimitOffsetPagination):
#     productinventory_serializer = ProductInventorySearchSerializer
#     search_document = ProductInventoryDocument

#     def get(self, request, query=None):
#         try:
#             q = Q(
#                 "multi_match",
#                 query=query,
#                 fields=["product.name", "product.web_id", "brand.name"],
#                 fuzziness="auto",
#             ) & Q(
#                 should=[
#                     Q("match", is_default=True),
#                 ],
#                 minimum_should_match=1,
#             )

#             search = self.search_document.search().query(q)
#             response = search.execute()

#             results = self.paginate_queryset(response, request, view=self)
#             serializer = self.productinventory_serializer(results, many=True)
#             return self.get_paginated_response(serializer.data)

#         except Exception as e:
#             return HttpResponse(e, status=500)
