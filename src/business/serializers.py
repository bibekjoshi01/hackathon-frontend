from rest_framework import serializers
from .models import BusinessDocuments, BusinessInfo, BusinessCategory


class BusinessCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessCategory
        fields = ["id", "name"]


class BusinessInfoSerializer(serializers.ModelSerializer):
    is_verified = serializers.SerializerMethodField()

    class Meta:
        model = BusinessInfo
        fields = [
            "category",
            "latitude",
            "longitude",
            "logo",
            "business_name",
            "description",
            "story",
            "contact_email",
            "contact_no",
            "is_verified",
        ]

    def get_is_verified(self, obj):
        try:
            return obj.documents.is_verified
        except BusinessDocuments.DoesNotExist:
            return False

class BusinessInfoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessInfo
        fields = [
            "category",
            "latitude",
            "longitude",
            "logo",
            "business_name",
            "description",
            "story",
            "contact_email",
            "contact_no",
        ]

    def create(self, validated_data):
        user = self.context["request"].user  
        if BusinessInfo.objects.filter(farmer=user).exists():
            raise serializers.ValidationError(
                "Business info already exists for this farmer."
            )

        business_info = BusinessInfo.objects.create(
            **validated_data, farmer=user, created_by=user
        )
        return business_info


class BusinessInfoRetrieveSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name")
    is_verified = serializers.SerializerMethodField()

    class Meta:
        model = BusinessInfo
        fields = [
            "category",
            "latitude",
            "longitude",
            "logo",
            "business_name",
            "description",
            "story",
            "contact_email",
            "contact_no",
            "is_verified",
        ]

    def get_is_verified(self, obj):
        try:
            return obj.documents.is_verified
        except BusinessDocuments.DoesNotExist:
            return False


class BusinessDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessDocuments
        fields = [
            "registration_certificate",
            "tax_certificate",
            "owner_id", 
            "address_proof",
        ]
