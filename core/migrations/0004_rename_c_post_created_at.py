# Generated by Django 5.1.1 on 2024-10-06 05:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_post_date_posted_post_c'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='C',
            new_name='created_at',
        ),
    ]