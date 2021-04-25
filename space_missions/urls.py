from django.urls import path
from . import views

app_name = 'space_missions'

urlpatterns = [
    path('countries/', views.CountryListView.as_view(), name='countries'),
    path('country/<str:pk>', views.CountryDetailView.as_view(), name='country-detail'),
    path('astronauts/', views.AstronautList.as_view(), name='astronauts'),
    path('astronaut/<str:pk>', views.AstronautDetail.as_view(), name='astronaut-detail'),
]
