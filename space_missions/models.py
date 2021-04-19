from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# Create your models here.

class Country(models.Model):
    code = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=40)
    continent = models.TextChoices('Continent', 'Africa Americas Asia Europe Oceania')


class Astronaut(models.Model):
    id = models.CharField(max_length=256, primary_key=True)
    name = models.CharField(max_length=40)
    original_name = models.CharField(max_length=40)

    SEX_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('U', 'Unspecified'))

    BACKGROUND_CHOICES = (
        ('M', 'Military'),
        ('C', 'Civilian'),
        ('U', 'Unspecified'))

    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    background = models.CharField(max_length=1, choices=BACKGROUND_CHOICES)
    year_of_birth = models.PositiveSmallIntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2010)])
    nationality =   models.ForeignKey('space_missions.Country', on_delete=models.CASCADE)

"""
class Selection(models.Model):
    # NB: Una missione può avere + programmi di selezione
    name       = models.CharField(max_length=40, primary_key=True)
    missions   = models.ManyToManyField('space_missions.Mission', on_delete=models.CASCADE)
    astronauts = models.ManyToManyField('space_missions.Astronaut',
                                        through='RecruitmentProcedure',
                                        related_name='selections',
                                        on_delete=models.CASCADE)


class RecruitmentProcedure(models.Model):
    class Meta:
        unique_together = [('astronaut', 'selection')]
    astronaut = models.ForeignKey('space_missions.Astronaut', on_delete=models.CASCADE)
    selection = models.ForeignKey('space_missions.Selection', on_delete=models.CASCADE)
    year_of_selection = models.PositiveSmallIntegerField()


class AstronautOccupation(models.Model):
    class Meta:
        unique_together = [('astronaut', 'mission')]
    astronaut = models.ForeignKey('space_missions.Astronaut', on_delete=models.CASCADE)
    mission = models.ForeignKey('space_missions.Mission', on_delete=models.CASCADE)
    role = models.CharField(max_length=40)
    year_of_join = models.PositiveSmallIntegerField()


class Launch(models.Model):
    SF_choices = ('Success', 'Fail', 'unknown')
    type_of_launch_choices = ('Orbital', 'DeepSpaceMission', 'unknown')

    id = models.CharField(max_length=10, primary_key=True)
    date = models.DateField()
    launch_vehicle = models.ForeignKey('space_missions.LaunchVehicle', on_delete=models.CASCADE)
    organization = models.ForeignKey('space_missions.Organization', on_delete=models.CASCADE)
    success_or_fail = models.CharField(max_length=20, choices=[(d, d) for d in SF_choices])
    type_of_launch = models.CharField(max_length=20, choices=[(d, d) for d in type_of_launch_choices])


class Mission(models.Model):
    launch = models.OneToOneField('space_missions.models.Launch', on_delete=models.CASCADE)
    name = models.CharField(max_length=30, primary_key=True)
    astronauts = models.ManyToManyField('space_missions.Astronaut',
                                        on_delete=models.CASCADE,
                                        through='AstronautOccupation',
                                        related_name='missions')
"""