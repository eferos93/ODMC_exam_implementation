from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('countries/', views.CountryListView.as_view(), name='countries'),
    path('country/<str:pk>', views.CountryDetailView.as_view(), name='country-detail'),
]