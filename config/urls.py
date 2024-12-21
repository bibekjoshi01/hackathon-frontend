# ruff: noqa
from django.urls import path
from django.urls import include
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularSwaggerView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


class CustomSpectacularSwaggerView(SpectacularSwaggerView):
    def dispatch(self, request, *args, **kwargs):
        from django.shortcuts import redirect
        from rest_framework.reverse import reverse

        response = super().dispatch(request, *args, **kwargs)
        if response.status_code == 401 or response.status_code == 403:
            # Redirect the user to the login page if not authenticated
            return redirect(reverse("rest_framework:login") + f"?next={request.path}")
        return response


api_url_patterns = [
    path("v1/admin/", include("src.api.admin.urls")),
    path("v1/public/", include("src.api.public.urls")),
]

urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # Media files
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()

# API URLS
urlpatterns += [
    # API base url
    path("api/", include(api_url_patterns)),
    # DRF auth token
    path("api-auth/", include("rest_framework.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        CustomSpectacularSwaggerView.as_view(url_name="api-schema"),
        name="swagger-ui",
    ),
]