# Create your views here.
from django.views import generic
from . import models


class CountryListView(generic.ListView):
    model = models.Country


class CountryDetailView(generic.DetailView):
    model = models.Country


class AstronautList(generic.ListView):
    model = models.Astronaut


class AstronautDetail(generic.DetailView):
    model = models.Astronaut
