# Generated by Django 3.0.8 on 2020-12-12 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health_institution', '0002_remove_healthinstitution_province'),
    ]

    operations = [
        migrations.AlterField(
            model_name='healthinstitution',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='healthinstitution',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='healthinstitution',
            name='website',
            field=models.URLField(null=True),
        ),
    ]
