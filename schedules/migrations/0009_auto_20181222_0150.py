# Generated by Django 2.1.4 on 2018-12-22 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0008_auto_20181222_0148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='dates',
            field=models.ManyToManyField(related_name='groups', to='schedules.Date'),
        ),
        migrations.AlterField(
            model_name='group',
            name='teachers',
            field=models.ManyToManyField(related_name='groups', to='schedules.Teacher'),
        ),
    ]