# Generated by Django 5.1 on 2024-09-13 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0013_avilableurl_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='avilableurl',
            name='category',
            field=models.ManyToManyField(blank=True, null=True, to='scraper.category'),
        ),
    ]
