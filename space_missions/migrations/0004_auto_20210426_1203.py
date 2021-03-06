# Generated by Django 3.2 on 2021-04-26 12:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('space_missions', '0003_auto_20210426_1144'),
    ]

    operations = [
        migrations.RenameField(
            model_name='astronautselection',
            old_name='year_of_selection',
            new_name='selection_year',
        ),
        migrations.AlterUniqueTogether(
            name='astronautselection',
            unique_together={('astronaut', 'selection', 'selection_year')},
        ),
    ]
