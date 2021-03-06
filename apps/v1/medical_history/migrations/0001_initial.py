# Generated by Django 3.1.4 on 2020-12-12 05:00

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('patient', '0002_auto_20201212_0835'),
    ]

    operations = [
        migrations.CreateModel(
            name='MedicalHistory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('relationship', models.PositiveSmallIntegerField(choices=[(1, 'Father'), (2, 'Mother')])),
                ('description', models.TextField(max_length=2000)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medical_histories', to='patient.patient')),
            ],
            options={
                'unique_together': {('patient', 'relationship')},
            },
        ),
    ]
