# Generated by Django 5.1.1 on 2024-10-02 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_inuser_phone_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='inuser',
            name='username',
            field=models.CharField(default='NAmaz', max_length=150, verbose_name='username'),
        ),
    ]
