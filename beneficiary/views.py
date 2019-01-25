from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Person
from user.models import CommunalCouncilLevel
from .forms import PersonForm

# Create your views here.

class PersonListView(ListView):

    model = Person
    template_name = 'beneficiary/person_list.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.profile.level == 5:
            return super(PersonListView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_queryset(self):
        communal_council_level = CommunalCouncilLevel.objects.get(profile=self.request.user.profile)
        if Person.objects.filter(communal_council_level=communal_council_level):
            queryset = Person.objects.filter(communal_council_level=communal_council_level)
            return queryset

class PersonCreateView(CreateView):
    model = Person
    form_class = PersonForm
    template_name = 'beneficiary/person_create.html'
    success_url = reverse_lazy('beneficiary:person_list')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.profile.level == 5:
            return super(PersonCreateView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        communal_council_level = CommunalCouncilLevel.objects.get(profile=self.request.user.profile)

        if form.cleaned_data['identity_card'] == '':
            self.object.identity_card = None

        if form.cleaned_data['email'] == '':
            self.object.email = None
        self.object.communal_council_level = communal_council_level
        self.object.save()
        return super(PersonCreateView, self).form_valid(form)

class PersonUpdateView(UpdateView):
    model = Person
    form_class = PersonForm
    template_name = 'beneficiary/person_create.html'
    success_url = reverse_lazy('beneficiary:person_list')

    def dispatch(self, request, *args, **kwargs):
        communal_council_level = CommunalCouncilLevel.objects.get(profile=self.request.user.profile)
        if self.request.user.profile.level == 5 and Person.objects.filter(pk=self.kwargs['pk'],communal_council_level=communal_council_level):
            return super(PersonUpdateView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_context_data(self, **kwargs):
        context = super(PersonUpdateView, self).get_context_data(**kwargs)
        context['diseases_list'] = self.object.diseases.all()
        context['disabilities_list'] = self.object.disabilities.all()
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if form.cleaned_data['identity_card'] == '':
            self.object.identity_card = None

        if form.cleaned_data['email'] == '':
            self.object.email = None
        self.object.save()
        return super(PersonUpdateView, self).form_valid(form)

class PersonDeleteView(DeleteView):
    model = Person
    template_name = 'beneficiary/person_delete.html'
    success_url = reverse_lazy('beneficiary:person_list')

    def dispatch(self, request, *args, **kwargs):
        communal_council_level = CommunalCouncilLevel.objects.get(profile=self.request.user.profile)
        if self.request.user.profile.level == 5 and Person.objects.filter(pk=self.kwargs['pk'],communal_council_level=communal_council_level):
            return super(PersonDeleteView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')
