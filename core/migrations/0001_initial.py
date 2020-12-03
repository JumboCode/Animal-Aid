# Generated by Django 2.2.16 on 2020-12-03 05:43

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FormDisplay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('displayed_form_id', models.IntegerField(default=1, verbose_name='displayed form id')),
            ],
        ),
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form_name', models.CharField(max_length=100)),
                ('pubdate', models.DateTimeField(verbose_name='date published')),
                ('walker_bool', models.BooleanField(default=1, verbose_name='form for walker info')),
                ('display_form', models.BooleanField(default=0, verbose_name='If form should be displayed')),
                ('form_display', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.FormDisplay')),
            ],
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(blank=True, max_length=200)),
                ('formType', models.CharField(choices=[('TF', 'Text Field'), ('CL', 'Checklist'), ('NM', 'Number'), ('DD', 'Dropdown Menu')], default='', max_length=20)),
                ('options', models.CharField(blank=True, max_length=200)),
                ('requiredBool', models.BooleanField(default=1, verbose_name='field required')),
                ('visibleBool', models.BooleanField(default=1, verbose_name='field visible')),
                ('order', models.IntegerField(blank=True, default=1, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='field order')),
                ('forms', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='field', to='core.Form')),
            ],
        ),
    ]
