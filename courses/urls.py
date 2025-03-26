from django.urls import path

from courses.views import get_course_info_view
from homepage.views import get_student_homepage_data_view


app_name = 'courses'

urlpatterns = [
    path('course-info/', get_course_info_view, name="get_course_info_view"),
    path('course-info/', get_interactive_coding_view, name="interactive_codding_view"),

]
