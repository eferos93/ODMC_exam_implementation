# Generated by Django 3.1.7 on 2021-04-21 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('space_missions', '0008_auto_20210421_1643'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organisation',
            name='t_start',
        ),
        migrations.RemoveField(
            model_name='organisation',
            name='t_stop',
        ),
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]