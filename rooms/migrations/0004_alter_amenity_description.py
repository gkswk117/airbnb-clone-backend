# Generated by Django 4.2.1 on 2023-05-16 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0003_room_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amenity',
            name='description',
            field=models.TextField(default=''),
        ),
    ]
