"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.urls import include, path
from rest_framework.permissions import AllowAny

from app.api import api_router

urlpatterns = [path("api/", include(api_router.urls))]

if settings.DEBUG:
    from django.contrib import admin
    from rest_framework.schemas import get_schema_view
    from rest_framework.documentation import include_docs_urls

    schema_view = get_schema_view(
        title="API documentation", permission_classes=[AllowAny]
    )
    urlpatterns += [
        path("admin/", admin.site.urls),
        path("api/", schema_view),
        path(
            "api/doc/",
            include_docs_urls(title="API documentation", permission_classes=[AllowAny]),
        ),
    ]
