from django.db import models

class Feedback(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    image = models.ImageField(upload_to="feedback", blank=True, null=True)
    role = models.CharField(max_length=255, blank=True, null=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    message = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.rating}"


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
