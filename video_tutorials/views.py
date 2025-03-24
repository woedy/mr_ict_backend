from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Recording, CodeSnapshot
from .serializers import RecordingSerializer, CodeSnapshotSerializer

class RecordingViewSet(viewsets.ModelViewSet):
    queryset = Recording.objects.all()
    serializer_class = RecordingSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CodeSnapshotViewSet(viewsets.ModelViewSet):
    queryset = CodeSnapshot.objects.all()
    serializer_class = CodeSnapshotSerializer
    
    def get_queryset(self):
        recording_id = self.request.query_params.get('recording_id')
        if recording_id:
            return CodeSnapshot.objects.filter(recording_id=recording_id)
        return CodeSnapshot.objects.all()
    
    @action(detail=False, methods=['post'])
    def create_batch(self, request):
        """Endpoint to create multiple snapshots at once"""
        snapshots = request.data
        serializer = self.get_serializer(data=snapshots, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    







from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Video
from .serializers import VideoSerializer

class VideoUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        # Debugging the request data
        print('####################')
        print(request.data)
        
        # Handle the uploaded video file
        video_file = request.FILES.get('video_file')  # Get the uploaded file from the request
        if video_file:
            print(f'File uploaded: {video_file.size}')
        
        file_serializer = VideoSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.decorators import api_view, permission_classes, authentication_classes



@api_view(['POST'])
def save_code_snapshot(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        code_content = request.data.get('code', "")
        cursor_position = request.data.get('cursorPosition', "")
        scroll_position = request.data.get('scrollPosition', "")
        timestamp = request.data.get('timestamp', "")

        # Validate input
        if not code_content:
            errors['code_content'] = ['Code content is required.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        new_snippet = CodeSnapshot.objects.create(
            code_content=code_content,
            cursor_position=cursor_position,
            scroll_position=scroll_position,
            timestamp=timestamp

        )

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)




