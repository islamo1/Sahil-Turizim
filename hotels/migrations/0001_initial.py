# Generated by Django 5.2 on 2025-05-08 19:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('url', models.URLField(blank=True)),
                ('rating', models.FloatField(blank=True, null=True)),
                ('view_type', models.CharField(blank=True, choices=[('city', 'City'), ('sea', 'Sea'), ('mountain', 'Mountain')], max_length=50)),
                ('room_type', models.CharField(blank=True, choices=[('single', 'Single'), ('double', 'Double'), ('suite', 'Suite'), ('apartment', 'Apartment')], max_length=50)),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotels.city')),
            ],
        ),
        migrations.CreateModel(
            name='HotelPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('num_guests', models.PositiveIntegerField(default=2)),
                ('price_usd', models.DecimalField(decimal_places=2, max_digits=6)),
                ('breakfast_included', models.BooleanField(default=False)),
                ('sea_view', models.BooleanField(default=False)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='hotels.hotel')),
            ],
            options={
                'ordering': ['start_date'],
            },
        ),
        migrations.CreateModel(
            name='Tour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_people', models.PositiveIntegerField()),
                ('has_kids', models.BooleanField(default=False, verbose_name='هل يوجد أطفال؟')),
                ('num_days', models.PositiveIntegerField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DailyPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_number', models.PositiveIntegerField()),
                ('activity', models.CharField(blank=True, max_length=255)),
                ('notes', models.TextField(blank=True)),
                ('hotel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hotels.hotel')),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='daily_plans', to='hotels.tour')),
            ],
        ),
        migrations.CreateModel(
            name='TourDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_number', models.PositiveIntegerField()),
                ('activity', models.CharField(blank=True, max_length=200)),
                ('note', models.TextField(blank=True)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotels.hotel')),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tour_days', to='hotels.tour')),
            ],
        ),
    ]
