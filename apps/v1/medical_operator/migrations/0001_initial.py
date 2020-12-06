# Generated by Django 3.1.4 on 2020-12-06 06:00

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('myauth', '0001_initial'),
        ('health_institution', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Operator',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='myauth.user')),
                ('birthday', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(message='The format should be dd/mm/yyyy', regex='^([1-9]|0[1-9]|[12]\\d|3[0-1])\\/([1-9]|0[1-9]|1[012])\\/[1-9]\\d+$')])),
                ('phone_number', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message='Invalid phone number', regex='^\\+[1-9]\\d{1,2}\\d{11,12}$')])),
                ('health_institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='health_institution.healthinstitution')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('myauth.user',),
        ),
    ]
