from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views import generic

from .models import Country

def index(request):
    """View function for home page of site."""
    context = {}
    return render(request, 'index.html', context=context)





class CountryListView(generic.ListView):
    model = Country


class CountryDetailView(generic.DetailView):
    """Generic class-based detail view for a book."""
    model = Country