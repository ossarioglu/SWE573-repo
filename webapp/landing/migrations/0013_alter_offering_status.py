# Generated by Django 3.2.9 on 2022-01-04 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0012_auto_20220104_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offering',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('Closed', 'Closed'), ('Assigned', 'Assigned')], default='New', editable=False, max_length=10),
        ),
    ]
