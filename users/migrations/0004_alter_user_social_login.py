# Generated by Django 4.2.1 on 2023-08-14 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_kakao_access_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='social_login',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
    ]