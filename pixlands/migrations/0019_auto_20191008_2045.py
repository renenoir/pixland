# Generated by Django 2.2.4 on 2019-10-08 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pixlands', '0018_auto_20191008_2044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date_added',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='like',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]