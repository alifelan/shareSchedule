# Generated by Django 2.1.4 on 2018-12-07 10:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0002_auto_20181207_1044'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='date',
            unique_together={('day', 'time')},
        ),
    ]
