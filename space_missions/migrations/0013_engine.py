# Generated by Django 3.2 on 2021-04-21 21:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('space_missions', '0012_delete_engine'),
    ]

    operations = [
        migrations.CreateModel(
            name='Engine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('mass', models.FloatField(blank=True, null=True)),
                ('impulse', models.FloatField(blank=True, null=True)),
                ('thrust', models.FloatField(blank=True, null=True)),
                ('isp', models.FloatField(blank=True, null=True)),
                ('burn_duration', models.FloatField(blank=True, null=True)),
                ('chambers', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('manufacturer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='space_missions.organisation')),
            ],
            options={
                'unique_together': {('name', 'manufacturer')},
            },
        ),
    ]
