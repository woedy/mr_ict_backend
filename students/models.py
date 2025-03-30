from django.db import models
from django.contrib.auth import get_user_model

from courses.models import ChallengeBadge, LessonCodeSnippet, CodingChallenge, Course, Lesson
from schools.models import School

User = get_user_model()

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.ForeignKey(School, related_name='students', on_delete=models.CASCADE)

    epz = models.IntegerField(default=0)

    is_archived = models.BooleanField(default=False)
    active = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)






class StudentCourse(models.Model):
    student = models.ForeignKey(Student, related_name='courses', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='courses', on_delete=models.CASCADE)

    completed = models.BooleanField(default=False)
    lessons_completed = models.IntegerField(default=0)
    total_lessons = models.IntegerField(default=0)
    progress_percent = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    
    is_archived = models.BooleanField(default=False)
    active = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"



class StudentCourseLesson(models.Model):
    course = models.ForeignKey(StudentCourse, related_name='student_course', on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, related_name='lesson', on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    resume_code = models.ForeignKey(LessonCodeSnippet, related_name='resume_code', on_delete=models.CASCADE)

    is_archived = models.BooleanField(default=False)
    active = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"



class LessonNote(models.Model):
    student = models.ForeignKey(Student, related_name='notes', on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, related_name='notes', on_delete=models.CASCADE)

    is_archived = models.BooleanField(default=False)
    active = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"
    



class LessonNoteSnippet(models.Model):
    note = models.ForeignKey(LessonNote, related_name='note_snippet', on_delete=models.CASCADE)
    snippet_interacted_with = models.ForeignKey(LessonCodeSnippet, related_name='code_snippet', on_delete=models.CASCADE)
    edited_code_content = models.TextField()

    completed = models.BooleanField(default=False)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)





class StudentChallenge(models.Model):
    student = models.ForeignKey(Student, related_name='challenges', on_delete=models.CASCADE)
    challenge = models.ForeignKey(CodingChallenge, related_name='student_challenges', on_delete=models.CASCADE)

    completed = models.BooleanField(default=False)

    
    is_archived = models.BooleanField(default=False)
    active = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"




class ResumeLeaning(models.Model):
    student = models.ForeignKey(Student, related_name='resume', on_delete=models.CASCADE)
    challenge = models.ForeignKey(CodingChallenge, related_name='challenges', on_delete=models.CASCADE)

    completed = models.BooleanField(default=False)

    
    is_archived = models.BooleanField(default=False)
    active = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"





class LessonFeedback(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='feedback', on_delete=models.CASCADE)
    student = models.ForeignKey(User, related_name='lesson_feedback', on_delete=models.CASCADE)
    feedback_text = models.TextField()

    is_archived = models.BooleanField(default=False)
    active = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Feedback for {self.lesson.title} by {self.student.username}"








class StudentBadge(models.Model):
    student = models.ForeignKey(User, related_name='badges', on_delete=models.CASCADE)
    badge = models.ForeignKey(ChallengeBadge, related_name='badge', on_delete=models.CASCADE)
    coding_challenge = models.ForeignKey(CodingChallenge, related_name='challenge', on_delete=models.CASCADE)

    earned_at = models.DateTimeField(auto_now_add=True)

    is_archived = models.BooleanField(default=False)
    active = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Badge {self.badge_name} earned by {self.student.username}"



