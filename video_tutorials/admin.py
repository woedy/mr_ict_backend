from django.contrib import admin

from video_tutorials.models import CodeSnapshot, Video

# Register your models here.
admin.site.register(Video)
admin.site.register(CodeSnapshot)