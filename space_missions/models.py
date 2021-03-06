from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify


# Create your models here.

class Country(models.Model):
    class Meta:
        ordering = ['name']

    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=40, null=True, blank=True)

    class Continent(models.TextChoices):
        AFRICA = 'Africa', _('Africa')
        AMERICAS = 'Americas', _('Americas')
        ASIA = 'Asia', _('Asia')
        EUROPE = 'Europe', _('Europe')
        OCEANIA = 'Oceania', _('Oceania')
        ANTARCTICA = 'Antarctica', _('Antarctica')

    continent = models.CharField(max_length=10, choices=Continent.choices, default=Continent.AMERICAS)

    def __str__(self):
        return self.name


class Astronaut(models.Model):
    class Meta:
        ordering = ['name']

    astronaut_id = models.CharField(max_length=256, unique=True)
    name = models.CharField(max_length=40)
    original_name = models.CharField(max_length=40)

    class SexOptions(models.TextChoices):
        MALE = 'M', _('Male')
        FEMALE = 'F', _('Female')
        UNSPECIFIED = 'U', _('Unspecified')

    class BackgroundOptions(models.TextChoices):
        MALE = 'M', _('Military')
        FEMALE = 'C', _('Civilian')
        UNSPECIFIED = 'U', _('Unspecified')

    sex = models.CharField(max_length=1, choices=SexOptions.choices, default=SexOptions.UNSPECIFIED)
    background = models.CharField(max_length=1, choices=BackgroundOptions.choices,
                                  default=BackgroundOptions.UNSPECIFIED)
    birth_year = models.PositiveSmallIntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2010)])
    nationality = models.ForeignKey('space_missions.Country', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Selection(models.Model):
    class Meta:
        ordering = ['name']

    name = models.CharField(max_length=40, unique=True)
    missions = models.ManyToManyField('space_missions.Mission')
    astronauts = models.ManyToManyField('space_missions.Astronaut',
                                        through='AstronautSelection',
                                        related_name='selections')

    def __str__(self):
        return self.name


class AstronautSelection(models.Model):
    class Meta:
        unique_together = [('astronaut', 'selection', 'selection_year')]
        ordering = ['astronaut', 'selection']

    astronaut = models.ForeignKey('space_missions.Astronaut', on_delete=models.CASCADE)
    selection = models.ForeignKey('space_missions.Selection', on_delete=models.CASCADE)
    selection_year = models.PositiveSmallIntegerField(validators=[MinValueValidator(1900),
                                                                  MaxValueValidator(timezone.now().year)]
                                                      )

    def __str__(self):
        return 'Astronaut: ' + str(self.astronaut) + '; Selection: ' + str(self.selection)


class AstronautOccupation(models.Model):
    class Meta:
        unique_together = [('astronaut', 'mission', 'role', 'join_year')]
        ordering = ['astronaut', 'mission']

    astronaut = models.ForeignKey('space_missions.Astronaut', on_delete=models.CASCADE)
    mission = models.ForeignKey('space_missions.Mission', on_delete=models.CASCADE)
    role = models.CharField(max_length=40)
    join_year = models.PositiveSmallIntegerField(validators=[MinValueValidator(1900),
                                                             MaxValueValidator(timezone.now().year)]
                                                 )

    def __str__(self):
        return 'Astronaut: ' + str(self.astronaut) + '; Mission: ' + str(self.mission)


class Launch(models.Model):
    class Meta:
        ordering = ['launch_id']

    SF_choices = ('Success', 'Fail', 'unknown')
    launch_types = ('Orbital', 'DeepSpaceMission', 'unknown')

    launch_id = models.CharField(max_length=10, unique=True)
    date = models.DateField()
    launch_vehicle = models.ForeignKey('space_missions.LaunchVehicle', on_delete=models.SET_NULL, null=True, blank=True)
    organisation = models.ForeignKey('space_missions.Organisation', on_delete=models.SET_NULL, null=True, blank=True)
    success_or_fail = models.CharField(max_length=20, choices=[(d, d) for d in SF_choices])
    launch_type = models.CharField(max_length=20, choices=[(d, d) for d in launch_types])

    def __str__(self):
        return self.launch_id


class Mission(models.Model):
    class Meta:
        ordering = ['name']

    launch = models.OneToOneField('space_missions.Launch', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=30, unique=True)
    astronauts = models.ManyToManyField('space_missions.Astronaut',
                                        blank=True,
                                        through='AstronautOccupation',
                                        related_name='missions')

    def __str__(self):
        return self.name


class LaunchVehicle(models.Model):
    class Meta:
        ordering = ['name']
    name = models.CharField(max_length=256, unique=True)
    min_stage = models.IntegerField(null=True, blank=True)
    max_stage = models.IntegerField(null=True, blank=True)
    launch_mass = models.FloatField(null=True, blank=True)
    TO_thrust = models.FloatField(null=True, blank=True)
    length = models.FloatField(null=True, blank=True)
    diameter = models.FloatField(null=True, blank=True)
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
    vehicle_class = models.CharField(max_length=1, choices=vehicle_classes, default='O')
    stages = models.ManyToManyField('space_missions.Stage', through='VehicleStage', blank=True)
    manufacturer = models.ForeignKey('space_missions.Organisation', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name


class Stage(models.Model):
    class Meta:
        ordering = ['name']

    name = models.CharField(max_length=256, unique=True)
    dry_mass = models.FloatField(null=True)
    launch_mass = models.FloatField(null=True)
    thrust = models.FloatField(null=True)
    burn_duration = models.FloatField(null=True)
    manufacturer = models.ForeignKey('space_missions.Organisation',
                                     on_delete=models.SET_NULL, null=True, blank=True)
    length = models.FloatField(null=True)
    diameter = models.FloatField(null=True)
    engine = models.ForeignKey('space_missions.Engine', on_delete=models.SET_NULL,
                               null=True, blank=True)

    def __str__(self):
        return self.name


class Engine(models.Model):
    class Meta:
        ordering = ['name']

    name = models.CharField(max_length=256, unique=True)
    manufacturer = models.ForeignKey('space_missions.Organisation', on_delete=models.SET_NULL, null=True, blank=True)
    mass = models.FloatField(null=True, blank=True)
    impulse = models.FloatField(null=True, blank=True)
    thrust = models.FloatField(null=True, blank=True)
    isp = models.FloatField(null=True, blank=True)
    burn_duration = models.FloatField(null=True, blank=True)
    chambers = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class VehicleStage(models.Model):
    class Meta:
        unique_together = [('launch_vehicle', 'stage', 'stage_number', 'dummy')]
        ordering = ['launch_vehicle', 'stage']
    launch_vehicle = models.ForeignKey('space_missions.LaunchVehicle', on_delete=models.CASCADE)
    stage = models.ForeignKey('space_missions.Stage', on_delete=models.CASCADE)
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
    stage_number = models.CharField(max_length=2, choices=stage_numbers)
    dummy = models.CharField(max_length=3, choices=[(value, value) for value in ['yes', 'no']])

    def __str__(self):
        return 'Vehicle: ' + str(self.launch_vehicle) + '; Stage: ' + str(self.stage)


class Organisation(models.Model):
    class Meta:
        ordering = ['name']

    code = models.CharField(max_length=256, unique=True)
    name = models.CharField(max_length=256, null=True)
    english_name = models.CharField(max_length=256, null=True)
    location = models.CharField(max_length=256, null=True)
    country = models.ForeignKey('space_missions.Country',
                                on_delete=models.SET_NULL, null=True, blank=True)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)
    parent_organisation = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
