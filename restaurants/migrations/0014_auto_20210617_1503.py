# Generated by Django 2.2 on 2021-06-17 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0013_auto_20210617_1457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='image',
            field=models.ImageField(upload_to='images'),
        ),
    ]
