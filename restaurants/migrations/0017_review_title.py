# Generated by Django 2.2 on 2021-06-18 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0016_review_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='title',
            field=models.CharField(default='', max_length=45),
            preserve_default=False,
        ),
    ]
