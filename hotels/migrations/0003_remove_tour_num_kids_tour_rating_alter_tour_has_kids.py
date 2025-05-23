# Generated by Django 5.2 on 2025-05-09 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0002_tour_num_kids'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tour',
            name='num_kids',
        ),
        migrations.AddField(
            model_name='tour',
            name='rating',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='tour',
            name='has_kids',
            field=models.BooleanField(default=False),
        ),
    ]
