# Generated by Django 2.2.16 on 2020-11-15 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_field_formtype'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='field',
            name='testBool',
        ),
        migrations.AddField(
            model_name='field',
            name='requiredBool',
            field=models.BooleanField(default=1, verbose_name='field required'),
        ),
        migrations.AddField(
            model_name='field',
            name='visibleBool',
            field=models.BooleanField(default=1, verbose_name='field visible'),
        ),
    ]
