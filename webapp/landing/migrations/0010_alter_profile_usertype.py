# Generated by Django 3.2.9 on 2022-01-04 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0009_auto_20220103_0011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='userType',
            field=models.CharField(choices=[('user', 'user'), ('admin', 'admin'), ('mentor', 'mentor')], default='user', max_length=10),
        ),
    ]