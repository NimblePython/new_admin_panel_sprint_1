# Generated by Django 3.2 on 2023-07-01 18:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_auto_20230701_1821'),
    ]

    operations = [
        migrations.RenameField(
            model_name='genrefilmwork',
            old_name='created',
            new_name='created_at',
        ),
    ]
