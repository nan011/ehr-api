# Generated by Django 3.1.4 on 2020-12-12 05:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0002_auto_20201212_0835'),
    ]

    operations = [
        migrations.RenameField(
            model_name='patient',
            old_name='physical_activity_type',
            new_name='physical_activity',
        ),
    ]
