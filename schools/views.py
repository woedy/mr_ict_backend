from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework.authentication import TokenAuthentication
from rest_framework import status

import random
import requests
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response

from schools.models import School


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def add_school_view(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        name = request.data.get('name', "")
        contact_email = request.data.get('contact_email', "")
        phone = request.data.get('phone', "")
        logo = request.data.get('logo', "")

        # Validate input
        if not name:
            errors['name'] = ['School Name required.']

        if not contact_email:
            errors['contact_email'] = ['Contact Email is required.']
            
        if not phone:
            errors['phone'] = ['Phone is required.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        # Generate unique phone numbers
        new_school = School.objects.create(
            name=name,
            contact_email=contact_email,
            logo=logo,
            phone=phone,
        )


        data['school_id'] = new_school.school_id
        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_all_schools_view(request):
    payload = {}
    data = {}
    errors = {}

    # Get query parameters
    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    # Start with all schools, excluding archived ones
    all_schools = School.objects.filter(is_archived=False)


    # If a search query is provided, filter by school name
    if search_query:
        all_schools = all_schools.filter(Q(name__icontains=search_query)).distinct()


    # Paginate the result
    paginator = Paginator(all_schools, page_size)

    try:
        paginated_schools = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_schools = paginator.page(1)
    except EmptyPage:
        paginated_schools = paginator.page(paginator.num_pages)

    # Serialize the paginated schools
    all_schools_serializer = AllSchoolsSerializer(paginated_schools, many=True)

    # Prepare the response data
    data['schools'] = all_schools_serializer.data
    data['pagination'] = {
        'page_number': paginated_schools.number,
        'total_pages': paginator.num_pages,
        'next': paginated_schools.next_page_number() if paginated_schools.has_next() else None,
        'previous': paginated_schools.previous_page_number() if paginated_schools.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


