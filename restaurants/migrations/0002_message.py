# Generated by Django 2.2 on 2021-06-16 17:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login_reg_app', '0001_initial'),
        ('restaurants', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creator_message', to='login_reg_app.User')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver_message', to='login_reg_app.User')),
            ],
        ),
    ]
