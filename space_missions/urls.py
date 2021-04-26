from django.urls import path
from . import views

app_name = 'space_missions'

urlpatterns = [
    path('countries/', views.CountryList.as_view(), name='countries'),
    path('country/<int:pk>', views.CountryDetail.as_view(), name='country-detail'),
    path('astronauts/', views.AstronautList.as_view(), name='astronauts'),
    path('astronaut/<int:pk>', views.AstronautDetail.as_view(), name='astronaut-detail'),
    path('organisations/', views.OrganisationList.as_view(), name='organisations'),
    path('organisation/<int:pk>', views.OrganisationDetail.as_view(), name='organisation-detail'),
    path('engines/', views.EngineList.as_view(), name='engines'),
    path('engine/<int:pk>', views.EngineDetail.as_view(), name='engine-detail'),
    path('stages/', views.StageList.as_view(), name='stages'),
    path('stage/<int:pk>', views.StageDetail.as_view(), name='stage-detail'),
    path('launchvehicles/', views.LaunchVehicleList.as_view(), name='launch-vehicles'),
    path('launchvehicle/<int:pk>', views.LaunchVehicleDetail.as_view(), name='launch-vehicle-detail'),
]
