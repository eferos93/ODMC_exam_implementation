from django.urls import path
from . import views

app_name = 'space_missions'

urlpatterns = [
    path('countries/', views.CountryListView.as_view(), name='countries'),
    path('country/<str:pk>', views.CountryDetailView.as_view(), name='country-detail'),
]
