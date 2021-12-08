# Generated by Django 3.2.9 on 2021-12-05 12:38

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offering',
            name='deadlineForUpdate',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 5, 12, 38, 0, 706841, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='offering',
            name='startingDate',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 5, 12, 38, 0, 706806, tzinfo=utc)),
        ),
    ]