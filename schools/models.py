from django.db import models
from django.db.models.signals import post_save, pre_save

from core.utils import unique_school_id_generator

class School(models.Model):
    school_id = models.CharField(max_length=20, unique=True)  # Unique code for each school
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='schools/', null=True, blank=True)
    contact_email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=255)

    
    is_archived = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


def pre_save_school_id_receiver(sender, instance, *args, **kwargs):
    if not instance.school_id:
        instance.school_id = unique_school_id_generator(instance)

pre_save.connect(pre_save_school_id_receiver, sender=School)



