# Generated by Django 5.1.7 on 2025-03-24 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_tutorials', '0005_codesnapshotrecording_delete_codesnapshot_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recording',
            name='timestamp',
        ),
        migrations.AlterField(
            model_name='recording',
            name='duration',
            field=models.FloatField(),
        ),
    ]
