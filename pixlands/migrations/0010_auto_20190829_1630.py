# Generated by Django 2.2.4 on 2019-08-29 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pixlands', '0009_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='photos/%Y/%m/%d'),
        ),
    ]
