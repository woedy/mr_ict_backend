from django.urls import path

from schools.views import add_school_view



app_name = 'schools'

urlpatterns = [
    path('add-school/', add_school_view, name="add_school_view"),
]
