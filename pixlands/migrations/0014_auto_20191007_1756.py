# Generated by Django 2.2.4 on 2019-10-07 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pixlands', '0013_auto_20191004_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=models.CharField(max_length=200),
        ),
    ]
