from rest_framework import serializers
from .models import Recording, CodeSnapshotRecording


class RecordingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recording
        fields = ["id", "title", "description", "video_file", "duration", "created_at"]

class AllRecordingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recording
        fields = ["id", "title", "video_file", "duration"]
        

class CodeSnapshotRecordingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeSnapshotRecording
        fields = [
            "id",
            "timestamp",
            "code_content",
            "cursor_position",
            "scroll_position",
            "is_highlight",
            "created_at",
        ]
