# Generated by Django 3.1.3 on 2021-02-06 21:24

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='day',
            field=models.CharField(default='c', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='match',
            name='time',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Walker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=100)),
                ('phone_number', models.IntegerField()),
                ('dog_1_nine_am', models.BooleanField()),
                ('dog_1_ten_am', models.BooleanField()),
                ('dog_1_eleven_am', models.BooleanField()),
                ('dog_1_noon', models.BooleanField()),
                ('dog_1_one_pm', models.BooleanField()),
                ('dog_1_two_pm', models.BooleanField()),
                ('dog_1_three_pm', models.BooleanField()),
                ('dog_1_four_pm', models.BooleanField()),
                ('dog_1_five_pm', models.BooleanField()),
                ('dog_2_nine_am', models.BooleanField()),
                ('dog_2_ten_am', models.BooleanField()),
                ('dog_2_eleven_am', models.BooleanField()),
                ('dog_2_noon', models.BooleanField()),
                ('dog_2_one_pm', models.BooleanField()),
                ('dog_2_two_pm', models.BooleanField()),
                ('dog_2_three_pm', models.BooleanField()),
                ('dog_2_four_pm', models.BooleanField()),
                ('dog_2_five_pm', models.BooleanField()),
                ('dog_3_nine_am', models.BooleanField()),
                ('dog_3_ten_am', models.BooleanField()),
                ('dog_3_eleven_am', models.BooleanField()),
                ('dog_3_noon', models.BooleanField()),
                ('dog_3_one_pm', models.BooleanField()),
                ('dog_3_two_pm', models.BooleanField()),
                ('dog_3_three_pm', models.BooleanField()),
                ('dog_3_four_pm', models.BooleanField()),
                ('dog_3_five_pm', models.BooleanField()),
                ('dog_4_nine_am', models.BooleanField()),
                ('dog_4_ten_am', models.BooleanField()),
                ('dog_4_eleven_am', models.BooleanField()),
                ('dog_4_noon', models.BooleanField()),
                ('dog_4_one_pm', models.BooleanField()),
                ('dog_4_two_pm', models.BooleanField()),
                ('dog_4_three_pm', models.BooleanField()),
                ('dog_4_four_pm', models.BooleanField()),
                ('dog_4_five_pm', models.BooleanField()),
                ('dog_5_nine_am', models.BooleanField()),
                ('dog_5_ten_am', models.BooleanField()),
                ('dog_5_eleven_am', models.BooleanField()),
                ('dog_5_noon', models.BooleanField()),
                ('dog_5_one_pm', models.BooleanField()),
                ('dog_5_two_pm', models.BooleanField()),
                ('dog_5_three_pm', models.BooleanField()),
                ('dog_5_four_pm', models.BooleanField()),
                ('dog_5_five_pm', models.BooleanField()),
                ('dog_1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dog1', to='core.dog')),
                ('dog_2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dog2', to='core.dog')),
                ('dog_3', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dog3', to='core.dog')),
                ('dog_4', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dog4', to='core.dog')),
                ('dog_5', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dog5', to='core.dog')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='match',
            name='walker',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='walker', to='core.walker'),
        ),
    ]
