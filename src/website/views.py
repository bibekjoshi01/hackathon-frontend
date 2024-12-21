from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Feedback
from .serializers import FeedbackSerializer, FeedbackRetrieveSerializer, NewsletterSubscriberSerializer


class CreateFeedbackAPI(APIView):
    permission_classes = [AllowAny]
    serializer_class = FeedbackSerializer

    def post(self, request):
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Feedback submitted successfully!"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetActiveFeedbackAPI(APIView):
    permission_classes = [AllowAny]
    serializer_class = FeedbackSerializer

    def get(self, request):
        feedbacks = Feedback.objects.filter(is_active=True)
        serializer = FeedbackRetrieveSerializer(feedbacks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubscribeNewsletterAPI(APIView):
    permission_classes = [AllowAny]
    serializer_class = NewsletterSubscriberSerializer

    def post(self, request):
        serializer = NewsletterSubscriberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Successfully subscribed to the newsletter!"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
