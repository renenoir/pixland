# Generated by Django 2.2.4 on 2019-10-14 12:17

from django.db import migrations, models
import pixlands.models


class Migration(migrations.Migration):

    dependencies = [
        ('pixlands', '0024_auto_20191014_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilepic',
            name='image',
            field=models.ImageField(blank=True, upload_to=pixlands.models.ProfilePic.user_directory_path),
        ),
    ]
