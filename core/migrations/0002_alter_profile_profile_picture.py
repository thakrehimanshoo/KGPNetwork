# Generated by Django 4.2.3 on 2024-05-06 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='static/profile_pics/user_icon.png', upload_to='static/profile_pics/'),
        ),
    ]
