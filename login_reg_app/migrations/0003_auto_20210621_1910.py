# Generated by Django 2.2 on 2021-06-22 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_reg_app', '0002_user_friends'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='friends',
            field=models.ManyToManyField(related_name='user_friends', to='login_reg_app.User'),
        ),
    ]
