# Generated by Django 3.1.4 on 2020-12-12 23:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lung_sound_classification', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lungsoundclassification',
            name='reserved_id',
            field=models.PositiveIntegerField(unique=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(9999)]),
        ),
    ]
