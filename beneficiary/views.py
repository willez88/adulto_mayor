from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Person
from user.models import CommunalCouncilLevel
from .forms import PersonForm

# Create your views here.

class PersonListView(ListView):

    model = Person
    template_name = 'beneficiary/person_list.html'

    def get_queryset(self):
        communal_council_level = CommunalCouncilLevel.objects.get(profile=self.request.user.profile)
        if Person.objects.filter(communal_council_level=communal_council_level):
            queryset = Person.objects.get(communal_council_level=communal_council_level)
            return queryset

class PersonCreateView(CreateView):
    model= Person
    form_class = PersonForm
    template_name = 'beneficiary/person_create.html'
    success_url = reverse_lazy('beneficiary:person_list')
