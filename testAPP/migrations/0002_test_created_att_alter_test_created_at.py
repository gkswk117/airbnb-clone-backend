# Generated by Django 4.2.1 on 2023-05-28 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testAPP', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='created_att',
            field=models.CharField(default='defualt', max_length=50),
        ),
        migrations.AlterField(
            model_name='test',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
