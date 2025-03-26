from django.db import models
from django.contrib.auth import get_user_model

from courses.models import Badge, CodeSnippet, CodingChallenge, Lesson
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









class StudentNote(models.Model):
    student = models.ForeignKey(Student, related_name='notes', on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, related_name='notes', on_delete=models.CASCADE)

    is_archived = models.BooleanField(default=False)
    active = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"
    



class StudentNoteSnippet(models.Model):
    note = models.ForeignKey(StudentNote, related_name='note_snippet', on_delete=models.CASCADE)
    snippet_interacted_with = models.ForeignKey(CodeSnippet, related_name='code_snippet', on_delete=models.CASCADE)
    edited_code_content = models.TextField()

    completed = models.BooleanField(default=False)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)








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
    badge = models.ForeignKey(Badge, related_name='badge', on_delete=models.CASCADE)
    coding_challenge = models.ForeignKey(CodingChallenge, related_name='challenge', on_delete=models.CASCADE)

    earned_at = models.DateTimeField(auto_now_add=True)

    is_archived = models.BooleanField(default=False)
    active = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Badge {self.badge_name} earned by {self.student.username}"



