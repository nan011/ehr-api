# Generated by Django 3.1.4 on 2020-12-06 00:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Province',
            fields=[
                ('basemodel_ptr', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='+', serialize=False, to='common.basemodel')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
            ],
            bases=('common.basemodel',),
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('basemodel_ptr', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='+', serialize=False, to='common.basemodel')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('province', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cities', to='area.province')),
            ],
            options={
                'verbose_name_plural': 'cities',
            },
            bases=('common.basemodel',),
        ),
    ]