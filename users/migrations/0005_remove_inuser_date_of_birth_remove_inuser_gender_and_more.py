# Generated by Django 5.1.1 on 2024-10-03 02:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_inuser_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inuser',
            name='date_of_birth',
        ),
        migrations.RemoveField(
            model_name='inuser',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='inuser',
            name='image',
        ),
        migrations.RemoveField(
            model_name='inuser',
            name='phone_num',
        ),
        migrations.RemoveField(
            model_name='inuser',
            name='username',
        ),
    ]