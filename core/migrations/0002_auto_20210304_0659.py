# Generated by Django 3.1.5 on 2021-03-04 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dog',
            name='dog_name',
            field=models.CharField(max_length=40),
        ),
    ]
