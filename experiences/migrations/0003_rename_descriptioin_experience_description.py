# Generated by Django 4.2.1 on 2023-08-14 18:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('experiences', '0002_experience_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='experience',
            old_name='descriptioin',
            new_name='description',
        ),
    ]
