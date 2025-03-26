from rest_framework.response import Response
from rest_framework import status

from video_tutorials.models import CodeSnapshotRecording, Recording
from rest_framework.decorators import api_view

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.contrib.auth import get_user_model

from django.conf import settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from video_tutorials.serializers import AllRecordingsSerializer


@api_view(['POST'])
#@permission_classes([IsAuthenticated])
#@authentication_classes([TokenAuthentication])
def record_video_view(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        title = request.data.get('title', "")
        description = request.data.get('description', "")
        video_file = request.FILES.get('video_file')
        duration = request.data.get('duration', "")

        # Validate input
        if not title:
            errors['title'] = ['Title is required.']

        if not description:
            errors['description'] = ['Description is required.']
 
        if not video_file:
            errors['video_file'] = ['Video is required.']
 
        if not duration:
            errors['duration'] = ['Duration is required.']
 

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)



        new_video = Recording.objects.create(
            title=title,
            description=description,
            video_file=video_file,
            duration=duration

        )

        data['video_id'] = new_video.id

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)







@api_view(['POST'])
def save_code_snapshot(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        title = request.data.get('title', "")
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


        new_snippet = CodeSnapshotRecording.objects.create(
            title=title,
            code_content=code_content,
            cursor_position=cursor_position,
            scroll_position=scroll_position,
            timestamp=timestamp

        )

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['GET'])
#@permission_classes([IsAuthenticated])
#@authentication_classes([TokenAuthentication])
def get_all_recorded_turorial_view(request):
    payload = {}
    data = {}
    errors = {}

  
    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 100

    
    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    all_tutorials = Recording.objects.all().filter().order_by('-id')


    if search_query:
        all_tutorials = all_tutorials.filter(
            Q(title__icontains=search_query) 
        )


    paginator = Paginator(all_tutorials, page_size)

    try:
        paginated_tutorials = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_tutorials = paginator.page(1)
    except EmptyPage:
        paginated_tutorials = paginator.page(paginator.num_pages)

    all_tutorials_serializer = AllRecordingsSerializer(paginated_tutorials, many=True)


    data['all_tutorials'] = all_tutorials_serializer.data

    data['pagination'] = {
        'page_number': paginated_tutorials.number,
        'count': all_tutorials.count(),
        'total_pages': paginator.num_pages,
        'next': paginated_tutorials.next_page_number() if paginated_tutorials.has_next() else None,
        'previous': paginated_tutorials.previous_page_number() if paginated_tutorials.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


