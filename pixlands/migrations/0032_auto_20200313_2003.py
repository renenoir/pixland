# Generated by Django 3.0.4 on 2020-03-13 17:03

from django.db import migrations, models
import pixlands.models


class Migration(migrations.Migration):

    dependencies = [
        ('pixlands', '0031_auto_20200313_1607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='photos/%Y/%m/%d', validators=[pixlands.models.Image.validate_image]),
        ),
    ]
