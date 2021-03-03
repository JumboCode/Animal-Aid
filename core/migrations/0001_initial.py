# Generated by Django 3.1.7 on 2021-03-01 19:49

import core.models
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import s3direct.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dog_name', models.CharField(max_length=30)),
                ('dog_info', models.CharField(max_length=200)),
                ('image_path', s3direct.fields.S3DirectField(blank=True)),
                ('owner_name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=100)),
                ('owner_phone', models.BigIntegerField(blank=True, null=True)),
                ('owner_email', models.CharField(max_length=100, null=True)),
                ('visible', models.BooleanField(default=True)),
                ('times', django.contrib.postgres.fields.ArrayField(base_field=models.BooleanField(), default=core.models.Dog.blank_times, size=63)),
            ],
            options={
                'ordering': ['dog_name'],
            },
        ),
        migrations.CreateModel(
            name='Walker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=100)),
                ('phone_number', models.BigIntegerField(blank=True, null=True)),
                ('dog_choices', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=16), default=core.models.Walker.blank_choices, size=None)),
                ('times', django.contrib.postgres.fields.ArrayField(base_field=models.BooleanField(), default=core.models.Walker.blank_times, size=63)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=10)),
                ('time', models.PositiveIntegerField()),
                ('dog', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dog', to='core.dog')),
                ('walker', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='walker', to='core.walker')),
            ],
        ),
    ]
