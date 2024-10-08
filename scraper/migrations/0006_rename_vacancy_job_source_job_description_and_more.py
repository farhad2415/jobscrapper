# Generated by Django 5.1 on 2024-09-10 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0005_job_job_type_job_location'),
    ]

    operations = [
        migrations.RenameField(
            model_name='job',
            old_name='vacancy',
            new_name='source',
        ),
        migrations.AddField(
            model_name='job',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='job_link',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='job_posted',
            field=models.DateField(blank=True, null=True),
        ),
    ]
