from django.db import models
from django.contrib.auth.models import User

class Recording(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video_file = models.FileField(upload_to='recordings/')
    duration = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class CodeSnapshot(models.Model):
    recording = models.ForeignKey(Recording, related_name='snapshots', on_delete=models.CASCADE)
    timestamp = models.FloatField()  # Seconds from start of video
    code_content = models.TextField()  # Full code at this timestamp
    cursor_position = models.JSONField(default=dict)  # e.g. {"line": 10, "column": 15}
    scroll_position = models.IntegerField(default=0)  # Pixel position
    is_highlight = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']







class Video(models.Model):
    video_file = models.FileField(upload_to='videos/')  # Store videos in a 'videos' folder
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Video {self.id} uploaded at {self.uploaded_at}'


class CodeSnapshot(models.Model):
    timestamp = models.FloatField()  # Seconds from start of video
    code_content = models.TextField()  # Full code at this timestamp
    cursor_position = models.JSONField(default=dict)  # e.g. {"line": 10, "column": 15}
    scroll_position = models.JSONField(default=dict)  # e.g. {"line": 10, "column": 15}

    is_highlight = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']
