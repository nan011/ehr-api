# Generated by Django 3.0.8 on 2020-12-12 01:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='height',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(999)]),
        ),
        migrations.AlterField(
            model_name='patient',
            name='nik',
            field=models.CharField(max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='physical_activity_type',
            field=models.IntegerField(choices=[(1, 'Light'), (2, 'Moderate'), (3, 'Heavy'), (4, 'Very Heavy')], default=1),
        ),
        migrations.AlterField(
            model_name='patient',
            name='smoke_amount',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='patient',
            name='weight',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(999)]),
        ),
    ]
