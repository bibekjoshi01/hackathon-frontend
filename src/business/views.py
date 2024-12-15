from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import BusinessInfo, BusinessCategory
from .serializers import (
    BusinessCategorySerializer,
    BusinessDocumentsSerializer,
    BusinessInfoCreateSerializer,
    BusinessInfoRetrieveSerializer,
    BusinessInfoSerializer,
)
from rest_framework.generics import ListAPIView
from rest_framework import serializers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter


class BusinessInfoCreateAPIView(generics.CreateAPIView):
    """
    API to create business info for a farmer.
    Ensures only one instance of BusinessInfo per farmer.
    """

    queryset = BusinessInfo.objects.all()
    serializer_class = BusinessInfoCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()


class BusinessInfoUpdateAPIView(generics.UpdateAPIView):
    """
    API to edit existing business info for a farmer.
    Only allows editing of the farmer's own business info.
    """

    queryset = BusinessInfo.objects.all()
    serializer_class = BusinessInfoSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        try:
            return BusinessInfo.objects.get(farmer=user)
        except BusinessInfo.DoesNotExist:
            raise serializers.ValidationError({"message": "Please add business info"})

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except serializers.ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class BusinessInfoRetrieveAPIView(generics.RetrieveAPIView):
    """
    API to retrieve existing business info for a farmer.
    """

    queryset = BusinessInfo.objects.all()
    serializer_class = BusinessInfoSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        try:
            business_info = BusinessInfo.objects.get(farmer=user)
        except BusinessInfo.DoesNotExist:
            raise serializers.ValidationError("Business info does not exist.")

        return business_info


class BusinessCategoryListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = BusinessCategory.objects.filter(is_active=True)
    serializer_class = BusinessCategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering = ["name"]
    search_fields = ["name"]
    ordering_fields = ["name"]


class BusinessInfoListAPIView(generics.RetrieveAPIView):
    """
    API to retrieve business info using farmer ID.
    """

    serializer_class = BusinessInfoRetrieveSerializer
    permission_classes = [AllowAny]

    def get(self, request, farmer_id, *args, **kwargs):
        business_info = get_object_or_404(BusinessInfo, farmer_id=farmer_id)
        serializer = self.get_serializer(business_info)
        return Response(serializer.data)


class SubmitBusinessKYCAPIView(generics.CreateAPIView):
    """
    API to submit KYC form for business verification.
    """

    serializer_class = BusinessDocumentsSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        business_info = get_object_or_404(BusinessInfo, farmer=user)
        if hasattr(business_info, "documents"):
            return Response(
                {"error": "KYC already submitted."}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(business=business_info, created_by=user)
            return Response(
                {"message": "KYC submitted successfully."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
