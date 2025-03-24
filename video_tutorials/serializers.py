from rest_framework import serializers
from .models import Recording, CodeSnapshot, Video

class CodeSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeSnapshot
        fields = ['id', 'recording', 'timestamp', 'code_content', 'cursor_position', 
                 'scroll_position', 'is_highlight', 'created_at']

class RecordingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recording
        fields = ['id', 'title', 'description', 'video_file', 'duration', 'created_at']
        read_only_fields = ['user']





class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['video_file', 'uploaded_at']
