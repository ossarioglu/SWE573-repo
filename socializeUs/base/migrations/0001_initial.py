# Generated by Django 3.2.9 on 2021-12-05 12:36

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Offering',
            fields=[
                ('serviceID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(default='New', max_length=10)),
                ('providerID', models.IntegerField()),
                ('keywords', models.CharField(max_length=100)),
                ('serviceInfo', models.CharField(blank=True, max_length=200, null=True)),
                ('startingDate', models.DateTimeField(default=datetime.datetime(2021, 12, 5, 12, 36, 2, 931022, tzinfo=utc))),
                ('duration', models.PositiveIntegerField(default=1)),
                ('meetingType', models.CharField(default='FaceToFace', max_length=10)),
                ('location', models.CharField(max_length=50)),
                ('capacity', models.PositiveIntegerField(default=1)),
                ('deadlineForUpdate', models.DateTimeField(default=datetime.datetime(2021, 12, 5, 12, 36, 2, 931062, tzinfo=utc))),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
