from rest_framework.response import Response
from rest_framework import status
import ffmpeg
import os
import tempfile
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

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

from video_tutorials.serializers import AllRecordingsSerializer, CodeSnapshotRecordingSerializer, RecordingSerializer



@api_view(['POST'])
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

        try:
            # Create a temporary file to store the uploaded video
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                tmp_file.write(video_file.read())
                tmp_file_path = tmp_file.name

            # Set the output path for the converted video (use a valid Windows path)
            output_path = f'C:/temp/{title}.mp4'  # Change this to your desired directory

            # Ensure the output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Perform the conversion
            ffmpeg.input(tmp_file_path).output(output_path).run()

            # Read the converted file and store it in Django storage
            with open(output_path, 'rb') as f:
                mp4_video = ContentFile(f.read(), name=f'{title}.mp4')
                video_path = default_storage.save(f'media/videos/{title}.mp4', mp4_video)

            # Delete the temporary files after conversion
            os.remove(tmp_file_path)
            os.remove(output_path)

            # Create the new video record in the database
            new_video = Recording.objects.create(
                title=title,
                description=description,
                video_file=video_path,
                duration=duration
            )

            #Set code snippet IDs
            # Use a batch update with `update()` to set the `recording` field for all matching records
            CodeSnapshotRecording.objects.filter(title=title).update(recording=new_video)

            data['video_id'] = new_video.id

            payload['message'] = "Successful"
            payload['data'] = data

        except Exception as e:
            payload['message'] = "Error during video conversion"
            payload['errors'] = str(e)
            return Response(payload, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(payload)



@api_view(['POST'])
def save_code_snapshot_orijay(request):
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



@api_view(['POST'])
def save_code_snapshot(request):
    """
    API endpoint to save batches of code snapshots
    """
    payload = {
        'message': '',
        'data': {},
        'errors': {},
        'success_count': 0,
        'error_count': 0
    }

    if request.method == 'POST':
        snapshots = request.data.get('snapshots', [])
        title = request.data.get('title', '')
        
        if not title:
            payload['errors']['title'] = ['Title is required.']
            payload['message'] = "Error: Missing title"
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        if not snapshots:
            payload['errors']['snapshots'] = ['No snapshots provided.']
            payload['message'] = "Error: No snapshots"
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        
        # Use bulk_create for better performance with multiple snapshots
        snapshots_to_create = []
        
        for index, snapshot in enumerate(snapshots):
            try:
                code_content = snapshot.get('code', "")
                cursor_position = snapshot.get('cursorPosition', {})
                scroll_position = snapshot.get('scrollPosition', {})
                timestamp = snapshot.get('timestamp', 0)
                
                if not code_content:
                    payload['error_count'] += 1
                    payload['errors'][f'snapshot_{index}'] = 'Code content is empty.'
                    continue
                
                # Prepare object for bulk creation
                snapshots_to_create.append(
                    CodeSnapshotRecording(
                        title=title,
                        code_content=code_content,
                        cursor_position=cursor_position,
                        scroll_position=scroll_position,
                        timestamp=timestamp
                    )
                )
                payload['success_count'] += 1
                
            except Exception as e:
                payload['error_count'] += 1
                payload['errors'][f'snapshot_{index}'] = str(e)
        
        # Bulk create all valid snapshots at once (more efficient)
        if snapshots_to_create:
            try:
                CodeSnapshotRecording.objects.bulk_create(snapshots_to_create)
                payload['message'] = f"Successfully saved {len(snapshots_to_create)} snapshots"
                payload['data']['saved_count'] = len(snapshots_to_create)
            except Exception as e:
                payload['message'] = f"Error during bulk save: {str(e)}"
                payload['errors']['bulk_save'] = str(e)
                return Response(payload, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            payload['message'] = "No valid snapshots to save"
            
    return Response(payload, status=status.HTTP_200_OK if payload['success_count'] > 0 else status.HTTP_400_BAD_REQUEST)




@api_view(['GET', ])
def get_video_tutorial_details_view(request):
    payload = {}
    data = {}
    errors = {}

    video_id = request.query_params.get('video_id', None)

    #if not video_id:
    #    errors['video_id'] = ["Video id required"]

    #try:
    #    _video = Recording.objects.get(video_id=video_id)
    #except Recording.DoesNotExist:
    #    errors['video_id'] = ['Recording does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    _video = Recording.objects.order_by('-id').first()



    data['video_url'] = _video.video_file.url


    code_snippets = CodeSnapshotRecording.objects.filter(recording=_video)
    code_snippets_serializer = CodeSnapshotRecordingSerializer(code_snippets, many=True)
    code_snippets = code_snippets_serializer.data if code_snippets_serializer else []

    data['code_snippets'] = code_snippets


    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


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





def cut_video_and_code(request):
    data = json.loads(request.body)
    video_id = data['videoId']
    start_time = data['start']
    end_time = data['end']

    # Step 1: Cut the video (you can use a library like moviepy or ffmpeg)
    # This utility function will handle video cutting and save the new video file
    cut_video(video_id, start_time, end_time)

    # Step 2: Remove code snapshots in the cut range
    CodeSnapshotRecording.objects.filter(
        timestamp__gte=start_time,
        timestamp__lte=end_time,
        video_id=video_id
    ).delete()  # This will delete all code snapshots that fall within the cut range

    # Step 3: Adjust the timestamps of the remaining code snapshots that are after the cut range
    CodeSnapshotRecording.objects.filter(
        timestamp__gt=end_time,
        video_id=video_id
    ).update(
        timestamp=F('timestamp') - (end_time - start_time)  # Adjust the timestamps
    )

    # Step 4: Optionally return the updated list of code snapshots
    remaining_snippets = CodeSnapshotRecording.objects.filter(video_id=video_id).values('id', 'timestamp', 'code_content', 'cursor_position', 'scroll_position')
    
    return JsonResponse({'updatedSnippets': list(remaining_snippets)})










#from moviepy.editor import VideoFileClip

def cut_video(video_id, start_time, end_time):
    video_path = f'/path/to/videos/{video_id}.mp4'
    output_path = f'/path/to/output/{video_id}_cut.mp4'
    
    video_clip = VideoFileClip(video_path)
    cut_clip = video_clip.subclip(start_time, end_time)
    cut_clip.write_videofile(output_path)
    
    # Optionally, update your video file path in the database if you want to store it
    # Video.objects.filter(id=video_id).update(video_file=output_path)
