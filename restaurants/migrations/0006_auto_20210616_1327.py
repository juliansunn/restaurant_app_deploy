# Generated by Django 2.2 on 2021-06-16 20:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0005_auto_20210616_1327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='location',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='restaurant_location', to='restaurants.Location'),
        ),
    ]
