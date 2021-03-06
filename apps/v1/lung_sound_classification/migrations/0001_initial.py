# Generated by Django 3.1.4 on 2020-12-12 22:34

import django.core.validators
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LungSoundClassification',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('reserved_id', models.DecimalField(decimal_places=0, max_digits=4, unique=True)),
                ('likelihood_percentage', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('result', models.PositiveSmallIntegerField(choices=[(99, 'Unclassified'), (1, 'Crackles'), (2, 'Wheezing')])),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
