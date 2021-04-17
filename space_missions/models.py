from django.core.validators import MinValueValidator
from django.db import models


# Create your models here.

class Country(models.Model):
    code = models.CharField(max_length=2)
    name = models.CharField(max_length=40)
    continent = models.TextChoices('Continent', 'Africa Americas Asia Europe Oceania')


class Astronaut(models.Model):
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
    nationality = models.ForeignKey('space_missions.Country', on_delete=models.CASCADE)


class Selection(models.Model):
    # NB: Una missione può avere + programmi di selezione
    name = models.CharField(max_length=40)
    missionname = models.ForeignKey('space_missions.Mission', on_delete=models.CASCADE)


class RecruitmentProcedure(models.Model):
    astronautID = models.ForeignKey('space_missions.Astronaut', on_delete=models.CASCADE)
    selectionID = models.ForeignKey('space_missions.Selection', on_delete=models.CASCADE)
    year_of_selection = models.PositiveSmallIntegerField()


class AstronautOccupation(models.Model):
    astronautID = models.ForeignKey('space_missions.Astronaut', on_delete=models.CASCADE)
    mission_title = models.ForeignKey('space_missions.Mission', on_delete=models.CASCADE)
    role_for_mission = models.CharField(max_length=40)
    year_of_join = models.PositiveSmallIntegerField()


class Launches(models.Model):
    SF_choices = ('Success', 'Fail', 'unknown')
    TypeOfLaunch_choices = ('Orbital', 'DeepSpaceMission', 'unknown')

    LaunchID = models.CharField(max_length=10)
    Date = models.DateField()
    LaunchVehicle = models.ForeignKey('space_missions.LaunchVehicle', on_delete=models.CASCADE)
    MissionID = models.ForeignKey('space_missions.Mission', on_delete=models.CASCADE)
    Organization = models.ForeignKey('space_missions.Organization', on_delete=models.CASCADE)
    SuccessOrFail = models.CharField(max_length=20, choices=[(d, d) for d in SF_choices])
    TypeOfLaunch = models.CharField(max_length=20, choices=[(d, d) for d in TypeOfLaunch_choices])


class Mission(models.Model):
    LaunchID = models.ForeignKey(Launches, on_delete=models.CASCADE)
    MissionID = models.CharField(max_length=30)
