from django.urls import path
from . import views

app_name = 'space_missions'

urlpatterns = [
    path('countries-metadata/', views.CountryMetadata.as_view(), name='countries'),
    path('countries/', views.CountryList.as_view(), name='countries-list'),
    path('country/<int:pk>/', views.CountryDetail.as_view(), name='country-detail'),
    path('countries/download-csv', views.download_countries_csv, name='countries-csv'),
    path('astronauts-metadata/', views.AstronautMetadata.as_view(), name='astronauts'),
    path('astronauts/', views.AstronautList.as_view(), name='astronauts-list'),
    path('astronaut/<int:pk>/', views.AstronautDetail.as_view(), name='astronaut-detail'),
    path('astronauts/download-csv', views.download_astronauts_csv, name='astronauts-csv'),
    path('astronautsoccupations/download-csv', views.download_astronaut_occupations_csv, name='astronautoccupations-csv'),
    path('astronautsselections/download-csv', views.download_astronauts_selections_csv, name='astroanutsselections-csv'),
    path('organisations/', views.OrganisationList.as_view(), name='organisations'),
    path('organisation/<int:pk>/', views.OrganisationDetail.as_view(), name='organisation-detail'),
    path('organisations/download-csv', views.download_organisations_csv, name='organisation-csv'),
    path('engines-metadata/', views.EngineMetadata.as_view(), name='engines'),
    path('engines/', views.EngineList.as_view(), name='engines-list'),
    path('engine/<int:pk>/', views.EngineDetail.as_view(), name='engine-detail'),
    path('engines/download-csv', views.download_engines_csv, name='engines-csv'),
    path('stages-metadata/', views.StageMetadata.as_view(), name='stages'),
    path('stages/', views.StageList.as_view(), name='stages-list'),
    path('stage/<int:pk>/', views.StageDetail.as_view(), name='stage-detail'),
    path('stages/download-csv', views.download_stages_csv, name='stages-csv'),
    path('launchvehicles-metadata/', views.LaunchVehicleMetadata.as_view(), name='launch-vehicles'),
    path('launchvehicles/', views.LaunchVehicleList.as_view(), name='launch-vehicles-list'),
    path('launchvehicle/<int:pk>/', views.LaunchVehicleDetail.as_view(), name='launch-vehicle-detail'),
    path('launchvehicles/download-csv', views.download_launch_vehicles_csv, name='launchvehicles-csv'),
    path('vehiclestages/download-csv', views.download_vehicle_stages_csv, name='vehiclestages-csv'),
    path('missions/', views.MissionList.as_view(), name='missions'),
    path('mission/<int:pk>/', views.MissionDetail.as_view(), name='mission-detail'),
    path('missions/download-csv', views.download_missions_csv, name='missions-csv'),
    path('selections/', views.SelectionList.as_view(), name='selections'),
    path('selection/<int:pk>/', views.SelectionDetail.as_view(), name='selection-detail'),
    path('selections/download-csv', views.download_selections_csv, name='selections-csv'),
]
