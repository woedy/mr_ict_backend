from django.db import models

class School(models.Model):
    name = models.CharField(max_length=255)
    school_code = models.CharField(max_length=20, unique=True)  # Unique code for each school
    logo = models.ImageField(upload_to='schools/', null=True, blank=True)
    contact_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)



class Teacher(models.Model):
    school = models.ForeignKey(School, related_name='teachers', on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)  # e.g., Python, JavaScript, etc.
    assigned_courses = models.ManyToManyField(Course)
    created_at = models.DateTimeField(auto_now_add=True)



class Classroom(models.Model):
    teacher = models.ForeignKey(Teacher, related_name='classrooms', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)  # e.g., "Grade 9 Python Class"
    class_code = models.CharField(max_length=20, unique=True)  # Unique class code
    students = models.ManyToManyField(Student)
    created_at = models.DateTimeField(auto_now_add=True)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.ForeignKey(School, related_name='students', on_delete=models.CASCADE)
    classrooms = models.ManyToManyField(Classroom)
    progress = models.JSONField()  # Stores progress data like lessons completed, quizzes passed, etc.
    created_at = models.DateTimeField(auto_now_add=True)





####################################################################



class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='course_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    video_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order = models.IntegerField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']





class Video(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='videos', on_delete=models.CASCADE)
    video_url = models.URLField()
    subtitles_url = models.URLField(null=True, blank=True)  # Optional for subtitles
    language = models.CharField(max_length=50, default='English')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Video for {self.lesson.title}"




class CodeSnippet(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='snippets', on_delete=models.CASCADE)
    code = models.TextField()  # Store the actual code
    timestamp = models.FloatField()  # Timestamp in the video when this code should appear (in seconds)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Snippet for {self.lesson.title} at {self.timestamp}s"



class UserProgress(models.Model):
    user = models.ForeignKey(User, related_name='progress', on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, related_name='progress', on_delete=models.CASCADE)
    snippets_interacted_with = models.ManyToManyField(CodeSnippet, blank=True)
    completed = models.BooleanField(default=False)
    started_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"





class UserProgress(models.Model):
    user = models.ForeignKey(User, related_name='progress', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='progress', on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, related_name='progress', on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    score = models.FloatField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.course.title} - {self.lesson.title}"






class CodingChallenge(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='challenges', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    instructions = models.TextField()
    expected_output = models.TextField(null=True, blank=True)
    code_template = models.TextField(null=True, blank=True)
    difficulty = models.CharField(max_length=10, choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title





class Assessment(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='assessments', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    passing_score = models.IntegerField()  # e.g., 70% passing grade
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title








class TeacherFeedback(models.Model):
    student = models.ForeignKey(User, related_name='feedbacks', on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, related_name='feedbacks', on_delete=models.CASCADE)
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.student.username} on {self.lesson.title}"








class Question(models.Model):
    assessment = models.ForeignKey(Assessment, related_name='questions', on_delete=models.CASCADE)
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=[('multiple_choice', 'Multiple Choice'), ('true_false', 'True/False')])
    options = models.JSONField(null=True, blank=True)  # Stores options for MCQs in JSON format
    correct_answer = models.TextField()

    def __str__(self):
        return self.question_text



class StudentQuizAttempt(models.Model):
    student = models.ForeignKey(User, related_name='quiz_attempts', on_delete=models.CASCADE)
    assessment = models.ForeignKey(Assessment, related_name='attempts', on_delete=models.CASCADE)
    answers = models.JSONField()  # Store the answers the student provided (JSON object)
    score = models.IntegerField()
    status = models.CharField(max_length=10, choices=[('passed', 'Passed'), ('failed', 'Failed')])
    attempted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attempt by {self.student.username} on {self.assessment.title}"


class LessonFeedback(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='feedback', on_delete=models.CASCADE)
    student = models.ForeignKey(User, related_name='lesson_feedback', on_delete=models.CASCADE)
    feedback_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.lesson.title} by {self.student.username}"


class Badge(models.Model):
    student = models.ForeignKey(User, related_name='badges', on_delete=models.CASCADE)
    badge_name = models.CharField(max_length=255)
    criteria = models.TextField()
    earned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Badge {self.badge_name} earned by {self.student.username}"
