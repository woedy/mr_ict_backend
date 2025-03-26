from django.db import models

class School(models.Model):
    name = models.CharField(max_length=255)
    school_code = models.CharField(max_length=20, unique=True)  # Unique code for each school
    logo = models.ImageField(upload_to='schools/', null=True, blank=True)
    contact_email = models.EmailField()
    
    is_archived = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)




