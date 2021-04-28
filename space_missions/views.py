# Create your views here.
import csv

from django.http import HttpResponse
from django.views import generic
from . import models
from .models import Organisation, Country, Astronaut, Engine, LaunchVehicle, VehicleStage, Mission, AstronautOccupation, \
    Selection, AstronautSelection, Stage


class CountryList(generic.ListView):
    model = models.Country


class CountryDetail(generic.DetailView):
    model = models.Country


class AstronautList(generic.ListView):
    model = models.Astronaut


class AstronautDetail(generic.DetailView):
    model = models.Astronaut


class OrganisationDetail(generic.DetailView):
    model = models.Organisation


class OrganisationList(generic.ListView):
    model = models.Organisation


class EngineList(generic.ListView):
    model = models.Engine


class EngineDetail(generic.DetailView):
    model = models.Engine


class StageDetail(generic.DetailView):
    model = models.Stage


class StageList(generic.ListView):
    model = models.Stage


class LaunchVehicleList(generic.ListView):
    model = models.LaunchVehicle


class LaunchVehicleDetail(generic.DetailView):
    model = models.LaunchVehicle


class MissionList(generic.ListView):
    model = models.Mission


class MissionDetail(generic.DetailView):
    model = models.Mission


class SelectionList(generic.ListView):
    model = models.Selection


class SelectionDetail(generic.DetailView):
    model = models.Selection


def download_organisations_csv(request):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="organisations.csv"'}
    )
    writer = csv.writer(response)
    writer.writerow(['code', 'name', 'english_name', 'location',
                     'country', 'longitude', 'latitude', 'parent_organisation']
                    )
    for organisation in Organisation.objects.all():
        parent_organisation = None if organisation.parent_organisation is None else organisation.parent_organisation.code
        country = None if organisation.country is None else organisation.country.code
        writer.writerow([organisation.code, organisation.name,
                         organisation.english_name, organisation.location,
                         country, organisation.longitude, organisation.latitude,
                         parent_organisation])
    return response


def download_countries_csv(request):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="countries.csv"'}
    )
    writer = csv.writer(response)
    writer.writerow(['code', 'name', 'continent'])
    for country in Country.objects.all():
        writer.writerow([country.code, country.name, country.continent])

    return response


def download_astronauts_csv(request):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="astronauts.csv"'}
    )
    writer = csv.writer(response)
    writer.writerow(['name', 'original_name', 'sex', 'background', 'birth_year', 'nationality'])
    for astronaut in Astronaut.objects.all():
        nationality = None if astronaut.nationality is None else astronaut.nationality.code
        writer.writerow([astronaut.name, astronaut.original_name, astronaut.get_sex_display(),
                         astronaut.get_background_display(), astronaut.birth_year,
                         nationality])

    return response


def download_engines_csv(request):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="engines.csv"'}
    )
    writer = csv.writer(response)
    writer.writerow(['name', 'manufacturer', 'mass', 'impulse', 'thrust', 'isp',
                     'burn_duration', 'chambers'])
    for engine in Engine.objects.all():
        manufacturer = None if engine.manufacturer is None else engine.manufacturer.code
        writer.writerow([engine.name, manufacturer, engine.mass,
                         engine.impulse, engine.thrust, engine.isp,
                         engine.burn_duration, engine.chambers])

    return response


def download_launch_vehicles_csv(request):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="LaunchVehicles.csv"'}
    )
    writer = csv.writer(response)
    writer.writerow(['name', 'min_stage', 'max_stage', 'launch_mass', 'TO_thrust',
                     'length', 'diameter', 'vehicle_class', 'manufacturer'])

    for vehicle in LaunchVehicle.objects.all():
        manufacturer = None if vehicle.manufacturer is None else vehicle.manufacturer.code
        writer.writerow([vehicle.name, vehicle.min_stage, vehicle.max_stage,
                         vehicle.launch_mass, vehicle.TO_thrust,
                         vehicle.length, vehicle.diameter, vehicle.get_vehicle_class_display(),
                         manufacturer])

    return response


def download_vehicle_stages_csv(request):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="VehicleStages.csv"'}
    )
    writer = csv.writer(response)
    writer.writerow(['launch_vehicle', 'stage', 'stage_number', 'dummy'])

    for vehicle_stage in VehicleStage.objects.all():
        writer.writerow([vehicle_stage.launch_vehicle.name, vehicle_stage.stage.name,
                         vehicle_stage.get_stage_number_display(),
                         vehicle_stage.dummy])

    return response


def download_missions_csv(request):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="Missions.csv"'}
    )
    writer = csv.writer(response)
    writer.writerow(['name', 'launch_id', 'date', 'launch_vehicle', 'organisation',
                     'success_or_fail', 'launch_type'])

    for mission in Mission.objects.all():
        launch_id = None if mission.launch is None else mission.launch.launch_id
        launch_date = None if mission.launch is None else mission.launch.date
        vehicle = None if mission.launch.launch_vehicle is None else mission.launch.launch_vehicle.name
        organisation = None if mission.launch.organisation is None else mission.launch.organisation.code
        writer.writerow([mission.name, launch_id, launch_date,
                         vehicle, organisation,
                         mission.launch.launch_type])

    return response


def download_astronaut_occupations_csv(request):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="AstronautOccupations.csv"'}
    )
    writer = csv.writer(response)
    writer.writerow(['astronaut', 'mission', 'role', 'join_year'])

    for astronaut_occupation in AstronautOccupation.objects.all():
        writer.writerow([astronaut_occupation.astronaut.name,
                         astronaut_occupation.mission.name,
                         astronaut_occupation.role, astronaut_occupation.join_year])

    return response


def download_selections_csv(request):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="selections.csv"'}
    )
    writer = csv.writer(response)
    writer.writerow(['name', 'mission'])

    for selection in Selection.objects.all():
        for mission in selection.missions.all():
            writer.writerow([selection.name, mission.name])

    return response


def download_astronauts_selections_csv(request):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="AstronautsSelections.csv"'}
    )
    writer = csv.writer(response)
    writer.writerow(['astronaut', 'selection', 'selection_year'])

    for astronaut_selection in AstronautSelection.objects.all():
        writer.writerow([astronaut_selection.astronaut.name, astronaut_selection.selection.name,
                         astronaut_selection.selection_year])
    return response


def download_stages_csv(request):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="Stages.csv"'}
    )
    writer = csv.writer(response)
    writer.writerow(['name', 'dry_mass', 'launch_mass', 'thrust', 'burn_duration',
                     'length', 'diameter', 'engine', 'manufacturer'])

    for stage in Stage.objects.all():
        manufacturer = None if stage.manufacturer is None else stage.manufacturer.code
        engine = None if stage.engine is None else stage.engine.name
        writer.writerow([stage.name, stage.dry_mass, stage.launch_mass, stage.thrust,
                         stage.burn_duration, stage.length, stage.diameter, engine,
                         manufacturer])
    return response

