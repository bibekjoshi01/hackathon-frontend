from rest_framework import serializers
from .models import Feedback, NewsletterSubscriber


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ["full_name", "email", "role", "rating", "message"]


class FeedbackRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ["full_name", "role", "image", "rating", "message", "created_at"]


class NewsletterSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']