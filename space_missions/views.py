from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views import generic

from . import models


# def index(request):
#     """View function for home page of site."""
#     context = {}
#     return render(request, '../templates/index.html', context=context)


class CountryListView(generic.ListView):
    model = models.Country


class CountryDetailView(generic.DetailView):
    model = models.Country
