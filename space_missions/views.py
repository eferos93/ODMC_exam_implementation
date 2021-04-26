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
