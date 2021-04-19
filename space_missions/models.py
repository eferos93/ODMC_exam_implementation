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
    nationality = models.ForeignKey('space_missions.Country', on_delete=models.CASCADE)


class Selection(models.Model):
    # NB: Una missione può avere + programmi di selezione
    name = models.CharField(max_length=40, primary_key=True)
    missions = models.ManyToManyField('space_missions.Mission', on_delete=models.CASCADE)
    astronauts = models.ManyToManyField('space_missions.Astronaut',
                                        through='space_missions.models.AstronautSelection',
                                        related_name='selections',
                                        on_delete=models.CASCADE)


class AstronautSelection(models.Model):
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
    organization = models.ForeignKey('space_missions.Organisation', on_delete=models.CASCADE)
    success_or_fail = models.CharField(max_length=20, choices=[(d, d) for d in SF_choices])
    type_of_launch = models.CharField(max_length=20, choices=[(d, d) for d in type_of_launch_choices])


class Mission(models.Model):
    launch = models.OneToOneField('space_missions.models.Launch', on_delete=models.CASCADE)
    name = models.CharField(max_length=30, primary_key=True)
    astronauts = models.ManyToManyField('space_missions.Astronaut',
                                        on_delete=models.CASCADE,
                                        through='AstronautOccupation',
                                        related_name='missions')


class LaunchVehicle(models.Model):
    name = models.CharField(max_length=256, primary_key=True)
    variant = models.CharField(max_length=256)
    alias = models.CharField(max_length=256)
    min_stage = models.IntegerField()
    max_stage = models.IntegerField()
    launch_mass = models.FloatField()
    TO_thrust = models.FloatField()

    vehicle_classes = [
        ('D', 'Extraterrestrial Deep Space Launch'),
        ('M', 'Missile'),
        ('O', 'Orbital Vehicle'),
        ('R', 'Research Rocket'),
        ('V', 'Reentry Test Vehicle'),
        ('X', 'Exoatmospheric test'),
        ('Y', 'Exoatmospheric weather rocket'),
        ('A', 'Endoatmospheric missile'),
        ('C', 'Cruise missile'),
        ('Q', 'Endoatmospheric reentry test vehicle'),
        ('T', 'Endoatmospheric test/research'),
        ('W', 'Endoatmospheric Weather rocket')
    ]
    vehicle_class = models.CharField(max_length=1,
                                     choices=vehicle_classes,
                                     default='O')
    measures = models.ForeignKey('space_missions.Measure', on_delete=models.SET_NULL)
    stages = models.ManyToManyField('space_missions.Stage',
                                    on_delete=models.CASCADE,
                                    through='VehicleStage')
    manufacturer = models.ForeignKey('space_missions.Organisation',
                                     on_delete=models.SET_NULL)


class Stage(models.Model):
    name = models.CharField(max_length=256, primary_key=True)
    dry_mass = models.FloatField()
    launch_mass = models.FloatField()
    thrust = models.FloatField()
    burn_duration = models.FloatField()
    manufacturer = models.ForeignKey('space_missions.Organisation',
                                     on_delete=models.SET_NULL)
    measures = models.ForeignKey('space_missions.Measure',
                                 on_delete=models.SET_NULL)


class Measure(models.Model):
    length = models.FloatField()
    diameter = models.FloatField()


class VehicleStage(models.Model):
    class Meta:
        unique_together = [('launch_vehicle', 'stage')]

    launch_vehicle = models.ForeignKey('space_missions.LaunchVehicle',
                                       on_delete=models.CASCADE)
    stage = models.ForeignKey('space_missions.Stage',
                              on_delete=models.CASCADE)
    stage_numbers = [
        ('-1', '-1'),
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('F', 'Fairing')
    ]

    stage_numbers = models.CharField(max_length=1, choices=stage_numbers)
    dummy = models.CharField(max_length=3, choices=['yes', 'no'])


class Organisation(models.Model):
    code = models.CharField(max_length=256, primary_key=True)
    U_code = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    english_name = models.CharField(max_length=256)
    location = models.CharField(max_length=256)
    t_start = models.DateField()
    t_stop = models.DateField()
    country = models.ForeignKey('space_missions.Country',
                                on_delete=models.CASCADE)
    coordinates = models.ForeignKey('space_missions.Coordinate',
                                    on_delete=models.SET_NULL)
    parent_organisation = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)


class Coordinate(models.Model):
    longitude = models.FloatField()
    latitude = models.FloatField()