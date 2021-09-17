from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from user.models import (
    CommunalCouncilLevel, MunicipalLevel, NationalLevel, ParishLevel,
    StateLevel,
)

from .forms import PersonForm
from .models import Person


class PersonListView(ListView):

    model = Person
    template_name = 'beneficiary/person_list.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.groups.filter(name='Nivel Nacional') or\
            self.request.user.groups.filter(name='Nivel Estadal') or\
            self.request.user.groups.filter(name='Nivel Municipal') or\
            self.request.user.groups.filter(name='Nivel Parroquial') or\
                self.request.user.groups.filter(name='Nivel Comunal'):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_queryset(self):

        # usuario nacional puede ver al nivel personas
        if NationalLevel.objects.filter(profile=self.request.user.profile):
            national_level = NationalLevel.objects.get(
                profile=self.request.user.profile
            )
            queryset = Person.objects.filter(
                communal_council_level__communal_council__parish__municipality__state__country=national_level.country
            )
            return queryset

        # usuario estadal puede ver al nivel personas
        if StateLevel.objects.filter(profile=self.request.user.profile):
            state_level = StateLevel.objects.get(
                profile=self.request.user.profile
            )
            queryset = Person.objects.filter(
                communal_council_level__communal_council__parish__municipality__state=state_level.state
            )
            return queryset

        # usuario municipal puede ver al nivel personas
        if MunicipalLevel.objects.filter(profile=self.request.user.profile):
            municipal_level = MunicipalLevel.objects.get(
                profile=self.request.user.profile
            )
            queryset = Person.objects.filter(
                communal_council_level__communal_council__parish__municipality=municipal_level.municipality
            )
            return queryset

        # usuario parroquial puede ver al nivel personas
        if ParishLevel.objects.filter(profile=self.request.user.profile):
            parish_level = ParishLevel.objects.get(
                profile=self.request.user.profile
            )
            queryset = Person.objects.filter(
                communal_council_level__communal_council__parish=parish_level.parish
            )
            return queryset

        if CommunalCouncilLevel.objects.get(profile=self.request.user.profile):
            communal_council_level = CommunalCouncilLevel.objects.get(
                profile=self.request.user.profile
            )
            queryset = Person.objects.filter(
                communal_council_level=communal_council_level
            )
            return queryset


class PersonCreateView(CreateView):
    model = Person
    form_class = PersonForm
    template_name = 'beneficiary/person_create.html'
    success_url = reverse_lazy('beneficiary:person_list')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.groups.filter(name='Nivel Comunal'):
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
        if CommunalCouncilLevel.objects.filter(
            profile=self.request.user.profile
        ):
            communal_council_level = CommunalCouncilLevel.objects.get(
                profile=self.request.user.profile
            )
            if self.request.user.groups.filter(name='Nivel Comunal') and\
                Person.objects.filter(
                    pk=self.kwargs['pk'],
                    communal_council_level=communal_council_level
            ):
                return super().dispatch(request, *args, **kwargs)
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
        if CommunalCouncilLevel.objects.filter(
            profile=self.request.user.profile
        ):
            communal_council_level = CommunalCouncilLevel.objects.get(
                profile=self.request.user.profile
            )
            if CommunalCouncilLevel.objects.filter(
                profile=self.request.user.profile
            ) and self.request.user.groups.filter(name='Nivel Comunal') and\
                Person.objects.filter(
                    pk=self.kwargs['pk'],
                    communal_council_level=communal_council_level):
                return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')
