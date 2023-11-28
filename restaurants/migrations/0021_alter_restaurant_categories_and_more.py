# Generated by Django 4.2.3 on 2023-07-18 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_reg_app', '0003_auto_20210621_1910'),
        ('restaurants', '0020_remove_restaurant_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='Category', to='restaurants.category'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='favorites',
            field=models.ManyToManyField(blank=True, related_name='favorites', to='login_reg_app.user'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='image_url',
            field=models.URLField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='transaction_types',
            field=models.ManyToManyField(blank=True, related_name='restaurant_transactions', to='restaurants.transactiontype'),
        ),
        migrations.AlterField(
            model_name='review',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='user_review_likes', to='login_reg_app.user'),
        ),
    ]