# Generated by Django 3.1.7 on 2021-04-22 12:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('space_missions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stage',
            name='engine',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='space_missions.engine'),
        ),
    ]
