# Generated by Django 4.2.1 on 2023-08-10 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_social_login_alter_user_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='kakao_access_token',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
