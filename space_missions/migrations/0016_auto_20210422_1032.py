# Generated by Django 3.1.7 on 2021-04-22 10:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('space_missions', '0015_stage_engine'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='engine',
            unique_together=set(),
        ),
    ]
