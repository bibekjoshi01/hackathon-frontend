from django.db import models

from src.base.models import AbstractInfoModel
from src.user.models import User


class BusinessCategory(AbstractInfoModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class BusinessInfo(AbstractInfoModel):
    farmer = models.OneToOneField(
        User, on_delete=models.PROTECT, related_name="business_info"
    )
    category = models.ForeignKey(BusinessCategory, on_delete=models.PROTECT)
    latitude = models.FloatField()
    longitude = models.FloatField()
    logo = models.ImageField(upload_to="business/logo", null=True)
    business_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    story = models.TextField(blank=True)
    contact_email = models.EmailField()
    contact_no = models.CharField(max_length=15)

    def __str__(self):
        return self.business_name


class BusinessDocuments(AbstractInfoModel):
    business = models.OneToOneField(
        BusinessInfo, on_delete=models.CASCADE, related_name="documents"
    )
    registration_certificate = models.FileField(
        upload_to="business_documents/registration/", blank=True, null=True
    )
    tax_certificate = models.FileField(
        upload_to="business_documents/tax/", blank=True, null=True
    )
    owner_id = models.FileField(
        upload_to="business_documents/owner_id/", blank=True, null=True
    )
    address_proof = models.FileField(
        upload_to="business_documents/address/", blank=True, null=True
    )
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"Documents for {self.business.business_name}"
