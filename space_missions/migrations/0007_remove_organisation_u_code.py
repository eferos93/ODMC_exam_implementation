# Generated by Django 3.1.7 on 2021-04-21 16:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('space_missions', '0006_auto_20210421_1620'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organisation',
            name='U_code',
        ),
    ]