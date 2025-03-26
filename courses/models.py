from django.db import models



class Course(models.Model):
    title = models.CharField(max_length=1000, unique=True,)
    description = models.TextField()
    image = models.ImageField(upload_to='course_images/')

    is_archived = models.BooleanField(default=False)
    active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=1000, unique=True)
    description = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)

    
    is_archived = models.BooleanField(default=False)
    active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    order = models.IntegerField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']




class LessonIntroVideo(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='intro_videos', on_delete=models.CASCADE)
    video_url = models.URLField()
    subtitles_url = models.URLField(null=True, blank=True)  # Optional for subtitles
    duration = models.FloatField()  # Seconds from start of video
    video_file = models.FileField(upload_to='lesson_intro_videos/')  # Store videos in a 'videos' folder
    language = models.CharField(max_length=50, default='English')

    is_archived = models.BooleanField(default=False)
    active = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Intro Video for {self.lesson.title}"





class LessonVideo(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='videos', on_delete=models.CASCADE)
    video_url = models.URLField()
    subtitles_url = models.URLField(null=True, blank=True)  # Optional for subtitles
    duration = models.FloatField()  # Seconds from start of video
    video_file = models.FileField(upload_to='lesson_videos/')  # Store videos in a 'videos' folder
    language = models.CharField(max_length=50, default='English')

    is_archived = models.BooleanField(default=False)
    active = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Video for {self.lesson.title}"




class LessonCodeSnippet(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='snippets', on_delete=models.CASCADE)

    title = models.CharField(max_length=1000)
    timestamp = models.FloatField()  # Seconds from start of video
    code_content = models.TextField()  # Full code at this timestamp
    cursor_position = models.JSONField(default=dict)  # e.g. {"line": 10, "column": 15}
    scroll_position = models.JSONField(default=dict)  # e.g. {"scrollTop": 0, "scrollLeft": 0}
    is_highlight = models.BooleanField(default=False)
    
    output = models.TextField(null=True, blank=True)


    is_archived = models.BooleanField(default=False)
    active = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Snippet for {self.lesson.title} at {self.timestamp}s"








class LessonAssignment(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='assignments', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    instructions = models.TextField()
    expected_output = models.TextField(null=True, blank=True)
    code_template = models.TextField(null=True, blank=True)
    difficulty = models.CharField(max_length=10, choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')])

    is_archived = models.BooleanField(default=False)
    active = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title






class CodingChallenge(models.Model):
    course = models.ForeignKey(Course, related_name='progress', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    instructions = models.TextField()
    expected_output = models.TextField(null=True, blank=True)
    code_template = models.TextField(null=True, blank=True)
    difficulty = models.CharField(max_length=10, choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')])

    is_archived = models.BooleanField(default=False)
    active = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title





class ChallengeBadge(models.Model):
    badge_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='badges/')
    criteria = models.TextField()

    def __str__(self):
        return f"Badge {self.badge_name} earned by {self.student.username}"
