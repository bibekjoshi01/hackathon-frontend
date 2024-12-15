from rest_framework import serializers

from src.product.models import Product, ProductCategory, ProductImage, ProductReview
from src.user.models import User


class FarmerListSerialier(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    contact_no = serializers.CharField(source="phone_no")

    class Meta:
        model = User
        fields = ["id", "full_name", "photo", "bio", "contact_no"]

    def get_full_name(self, obj):
        return obj.full_name


class UserListSerialier(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "full_name", "photo"]

    def get_full_name(self, obj):
        return obj.full_name


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image"]


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ["id", "name", "slug", "description"]


class ProductReviewsSerializer(serializers.ModelSerializer):
    created_by = UserListSerialier()

    class Meta:
        model = ProductReview
        fields = ["id", "rating", "review_message", "created_by"]


class PublicProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name")
    average_rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "farmer",
            "category_name",
            "name",
            "description",
            "price",
            "offer_price",
            "stock_quantity",
            "unit",
            "featured_image",
            "average_rating",
            "total_reviews",
        ]

    def get_average_rating(self, obj):
        return obj.average_rating()

    def get_total_reviews(self, obj):
        return obj.total_reviews()


class PublicProductRetrieveSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name")
    average_rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()
    reviews = ProductReviewsSerializer(many=True)
    farmer = FarmerListSerialier()

    class Meta:
        model = Product
        fields = [
            "id",
            "farmer",
            "category_name",
            "name",
            "description",
            "price",
            "offer_price",
            "stock_quantity",
            "unit",
            "featured_image",
            "average_rating",
            "total_reviews",
            "reviews",
        ]

    def get_average_rating(self, obj):
        return obj.average_rating()

    def get_total_reviews(self, obj):
        return obj.total_reviews()


class ProductReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = ["product", "rating", "review_message"]
