# Generated by Django 2.2 on 2021-06-16 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0009_auto_20210616_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='image_url',
            field=models.URLField(default=None, null=True),
        ),
    ]
