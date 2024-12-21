from django.urls import path
from .views import CreateFeedbackAPI, GetActiveFeedbackAPI, SubscribeNewsletterAPI

urlpatterns = [
    path("feedback/create", CreateFeedbackAPI.as_view(), name="create-feedback"),
    path("feedbacks", GetActiveFeedbackAPI.as_view(), name="get-active-feedback"),
    path(
        "newsletter/subscribe",
        SubscribeNewsletterAPI.as_view(),
        name="subscribe-newsletter",
    ),
]
