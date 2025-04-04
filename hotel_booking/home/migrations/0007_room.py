# Generated by Django 5.0.7 on 2025-03-05 14:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20250303_1432'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_rent', models.DecimalField(decimal_places=2, max_digits=10)),
                ('room_details', models.TextField()),
                ('available_room', models.IntegerField()),
                ('room_image', models.ImageField(upload_to='room_images/')),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='home.subcategory')),
            ],
        ),
    ]
