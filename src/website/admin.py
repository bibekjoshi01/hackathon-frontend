from django.contrib import admin
from . models import Feedback, NewsletterSubscriber


admin.site.site_header = "Parkify"
admin.site.site_title = "Parkify Admin Portal"
admin.site.index_title = "Welcome to Parkify Admin"


admin.site.register(Feedback)
admin.site.register(NewsletterSubscriber)
