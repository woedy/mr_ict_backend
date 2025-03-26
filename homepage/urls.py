from django.urls import path

from homepage.views import get_student_homepage_data_view


app_name = 'homepage'

urlpatterns = [
    path('student-homepage-data/', get_student_homepage_data_view, name="get_student_homepage_data_view"),

]
