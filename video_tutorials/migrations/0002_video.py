# Generated by Django 5.1.7 on 2025-03-24 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_tutorials', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_file', models.FileField(upload_to='videos/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
