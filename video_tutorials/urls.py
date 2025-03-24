from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecordingViewSet, CodeSnapshotViewSet, VideoUploadView



urlpatterns = [
    #path('api/', include(router.urls)),
    path('api/upload/', VideoUploadView.as_view(), name='video-upload'),


]