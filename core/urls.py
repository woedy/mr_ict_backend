"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

from video_tutorials.views import get_all_recorded_turorial_view, get_video_tutorial_details_view, record_video_view, save_code_snapshot


urlpatterns = [
    path("admin/", admin.site.urls),

    path('api/schools/', include('schools.urls', 'schools_api')),


    #path("api/upload/", VideoUploadView.as_view(), name="video-upload"),
    path("api/upload/", record_video_view, name="video-upload"),

    path("api/save-code-snapshots/", save_code_snapshot, name="save_code_snapshot"),

    path("api/all-recorded-videos/", get_all_recorded_turorial_view, name="all_recorded"),
    path("api/tutorial/", get_video_tutorial_details_view, name="video_code"),

]


if settings.DEBUG:
    urlpatterns = urlpatterns + static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    urlpatterns = urlpatterns + static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
