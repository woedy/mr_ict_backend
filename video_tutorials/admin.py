from django.contrib import admin

from video_tutorials.models import CodeSnapshotRecording, Recording

# Register your models here.
admin.site.register(Recording)
admin.site.register(CodeSnapshotRecording)