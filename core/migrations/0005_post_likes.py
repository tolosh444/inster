# Generated by Django 5.1.1 on 2024-10-13 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_rename_c_post_created_at'),
        ('users', '0008_alter_inuser_image_alter_inuser_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked_posts', to='users.inuser'),
        ),
    ]