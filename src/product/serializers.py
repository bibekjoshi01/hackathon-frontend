from rest_framework import serializers

from src.libs.get_context import get_user_by_context

from .models import Product, ProductCategory, ProductImage
from src.base.serializers import AbstractInfoRetrieveSerializer


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ["id", "name"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image"]


class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name")

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "category",
            "featured_image",
            "price",
            "offer_price",
            "unit",
            "is_active",
            "stock_quantity",
        ]


class ProductRetrieveSerializer(AbstractInfoRetrieveSerializer):
    category = ProductCategorySerializer()
    average_rating = serializers.SerializerMethodField() 

    class Meta(AbstractInfoRetrieveSerializer.Meta):
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "offer_price",
            "unit",
            "featured_image",
            "stock_quantity",
            "is_active",
            "description",
            "category",
            "average_rating"
        ]

        fields += AbstractInfoRetrieveSerializer.Meta.fields

    def get_average_rating(self, obj):
        return obj.average_rating()


class ProductCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=ProductCategory.objects.filter(is_active=True)
    )

    class Meta:
        model = Product
        fields = [
            "name",
            "price",
            "offer_price",
            "unit",
            "stock_quantity",
            "featured_image",
            "description",
            "category",
        ]

    def create(self, validated_data):
        category = validated_data.pop('category')
        featured_image = validated_data.pop('featured_image', None)
        user = get_user_by_context(self.context)
        validated_data["farmer"] = user
        validated_data["created_by"] = user
    
        product = Product.objects.create(category=category, **validated_data)

        if featured_image:
            product.featured_image = featured_image
            product.save()

        return product


class ProductUpdateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=ProductCategory.objects.filter(is_active=True)
    )

    class Meta:
        model = Product
        fields = [
            "name",
            "price",
            "offer_price",
            "unit",
            "stock_quantity",
            "featured_image",
            "is_active",
            "description",
            "category",
        ]
    
    def update(self, instance, validated_data):
        # Update the featured image if it exists in validated_data
        featured_image = validated_data.pop('featured_image', None)
        user = get_user_by_context(self.context)
        validated_data["updated_by"] = user
    
        if featured_image:
            instance.featured_image = featured_image

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance