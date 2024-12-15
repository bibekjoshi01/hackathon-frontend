from django.db import models
from src.base.models import AbstractInfoModel
from django.core.validators import MinValueValidator, MaxValueValidator

from src.user.models import User


class ProductCategory(AbstractInfoModel):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "product categories"
        ordering = ["-id"]

    def __str__(self) -> str:
        return self.name


class Product(AbstractInfoModel):
    UNIT_CHOICES = [
        ("kg", "Kilogram"),
        ("piece", "Piece"),
        ("litre", "Litre"),
        ("dozen", "Dozen"),
        ("pack", "Pack"),
    ]

    farmer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="products"
    )
    category = models.ForeignKey(
        ProductCategory, on_delete=models.SET_NULL, null=True, related_name="products"
    )
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()
    featured_image = models.ImageField(upload_to="products", null=True)
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default="piece")

    def __str__(self):
        return self.name

    def average_rating(self):
        reviews = self.reviews.all()
        total_reviews = reviews.count()
        if total_reviews == 0:
            return 0  # Return 0 if no reviews exist
        total_rating = sum(review.rating for review in reviews)
        return total_rating / total_reviews
    
    def total_reviews(self):
        return self.reviews.count()


class ProductReview(AbstractInfoModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], default=5
    )
    review_message = models.CharField(max_length=500)

    def __str__(self):
        return self.review_message


# Product Image Model
class ProductImage(AbstractInfoModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="product_images/")

    def __str__(self):
        return f"Image for {self.product.name}"


# Recommendation Data

class ProductSearch(models.Model):
    query = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Search {self.query}"


class ProductClick(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="clicks")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"clicked on {self.product.name}"

