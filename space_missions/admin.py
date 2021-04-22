from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Country)
admin.site.register(models.AstronautSelection)
admin.site.register(models.Astronaut)
admin.site.register(models.AstronautOccupation)
admin.site.register(models.Launch)
admin.site.register(models.LaunchVehicle)
admin.site.register(models.Mission)
admin.site.register(models.Organisation)
admin.site.register(models.Selection)
admin.site.register(models.Stage)
admin.site.register(models.VehicleStage)
admin.site.register(models.Engine)

