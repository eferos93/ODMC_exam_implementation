from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


# Create your models here.

class Country(models.Model):
    code = models.CharField(max_length=2, primary_key=True)
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
        return str(self.code) + " " + str(self.name) + " " + str(self.continent)


class Astronaut(models.Model):
    id = models.CharField(max_length=256, primary_key=True)
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
    year_of_birth = models.PositiveSmallIntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2010)])
    nationality = models.ForeignKey('space_missions.Country', on_delete=models.SET_NULL, null=True, blank=True)


class Selection(models.Model):
    # NB: Una missione può avere + programmi di selezione
    name = models.CharField(max_length=40, primary_key=True)
    missions = models.ManyToManyField('space_missions.Mission')
    astronauts = models.ManyToManyField('space_missions.Astronaut',
                                        through='AstronautSelection',
                                        related_name='selections')


class AstronautSelection(models.Model):
    class Meta:
        unique_together = [('astronaut', 'selection')]

    astronaut = models.ForeignKey('space_missions.Astronaut', on_delete=models.CASCADE)
    selection = models.ForeignKey('space_missions.Selection', on_delete=models.CASCADE)
    year_of_selection = models.PositiveSmallIntegerField(validators=[MinValueValidator(1900),
                                                                     MaxValueValidator(timezone.now().year)]
                                                         )


class AstronautOccupation(models.Model):
    class Meta:
        unique_together = [('astronaut', 'mission')]

    astronaut = models.ForeignKey('space_missions.Astronaut', on_delete=models.CASCADE)
    mission = models.ForeignKey('space_missions.Mission', on_delete=models.CASCADE)
    role = models.CharField(max_length=40)
    year_of_join = models.PositiveSmallIntegerField(validators=[MinValueValidator(1900),
                                                                MaxValueValidator(timezone.now().year)]
                                                    )


class Launch(models.Model):
    SF_choices = ('Success', 'Fail', 'unknown')
    types_of_launch = ('Orbital', 'DeepSpaceMission', 'unknown')

    id = models.CharField(max_length=10, primary_key=True)
    date = models.DateField()
    launch_vehicle = models.ForeignKey('space_missions.LaunchVehicle', on_delete=models.SET_NULL, null=True, blank=True)
    organisation = models.ForeignKey('space_missions.Organisation', on_delete=models.SET_NULL, null=True, blank=True)
    success_or_fail = models.CharField(max_length=20, choices=[(d, d) for d in SF_choices])
    type_of_launch = models.CharField(max_length=20, choices=[(d, d) for d in types_of_launch])


class Mission(models.Model):
    launch = models.OneToOneField('space_missions.Launch', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=30, primary_key=True)
    astronauts = models.ManyToManyField('space_missions.Astronaut',
                                        blank=True,
                                        through='AstronautOccupation',
                                        related_name='missions')


class LaunchVehicle(models.Model):
    name = models.CharField(max_length=256, primary_key=True)
    variant = models.CharField(max_length=256)
    alias = models.CharField(max_length=256)
    min_stage = models.IntegerField(null=True)
    max_stage = models.IntegerField(null=True)
    launch_mass = models.FloatField(null=True)
    TO_thrust = models.FloatField(null=True)
    length = models.FloatField(null=True)
    diameter = models.FloatField(null=True)

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
    stages = models.ManyToManyField('space_missions.Stage',
                                    through='VehicleStage', blank=True)
    manufacturer = models.ForeignKey('space_missions.Organisation',
                                     on_delete=models.SET_NULL, blank=True, null=True)


class Stage(models.Model):
    name = models.CharField(max_length=256, primary_key=True)
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


class Engine(models.Model):
    name = models.CharField(max_length=256, primary_key=True)
    manufacturer = models.ForeignKey('space_missions.Organisation', on_delete=models.SET_NULL, null=True, blank=True)
    mass = models.FloatField(null=True, blank=True)
    impulse = models.FloatField(null=True, blank=True)
    thrust = models.FloatField(null=True, blank=True)
    isp = models.FloatField(null=True, blank=True)
    burn_duration = models.FloatField(null=True, blank=True)
    chambers = models.PositiveSmallIntegerField(null=True, blank=True)


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

    stage_number = models.CharField(max_length=2, choices=stage_numbers)
    dummy = models.CharField(max_length=3, choices=[(value, value) for value in ['yes', 'no']])


class Organisation(models.Model):
    code = models.CharField(max_length=256, primary_key=True)
    name = models.CharField(max_length=256, null=True)
    english_name = models.CharField(max_length=256, null=True)
    location = models.CharField(max_length=256, null=True)
    country = models.ForeignKey('space_missions.Country',
                                on_delete=models.SET_NULL, null=True, blank=True)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)
    parent_organisation = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
