# Generated by Django 3.2 on 2023-07-01 18:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='filmwork',
            old_name='created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='filmwork',
            old_name='modified',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='genre',
            old_name='created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='genre',
            old_name='modified',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='person',
            old_name='created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='person',
            old_name='modified',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='personfilmwork',
            old_name='created',
            new_name='created_at',
        ),
    ]
