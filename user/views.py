from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import (
    NationalLevelUpdateForm, StateLevelForm, StateLevelUpdateForm, MunicipalLevelForm,
    ParishLevelForm, MunicipalLevelUpdateForm, ParishLevelUpdateForm,
    CommunalCouncilLevelForm, CommunalCouncilLevelUpdateForm
)
from .models import Profile, NationalLevel, StateLevel, MunicipalLevel, ParishLevel, CommunalCouncilLevel
from django.contrib.auth.models import User
from base.models import State, Municipality, Parish, CommunalCouncil
from django.conf import settings
from base.constant import EMAIL_SUBJECT
from base.functions import send_email
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.shortcuts import get_current_site
import logging
logger = logging.getLogger('user')

class NationalLevelUpdateView(UpdateView):
    model = User
    form_class = NationalLevelUpdateForm
    template_name = 'user/national.level.update.html'
    success_url = reverse_lazy('base:home')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.id == self.kwargs['pk'] and self.request.user.profile.level == 1:
            return super(NationalLevelUpdateView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_initial(self):
        initial_data = super(NationalLevelUpdateView, self).get_initial()
        initial_data['phone'] = self.object.profile.phone
        national_level = NationalLevel.objects.get(profile=self.object.profile)
        initial_data['country'] = national_level.country
        return initial_data

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.username = form.cleaned_data['username']
        self.object.first_name = form.cleaned_data['first_name']
        self.object.last_name = form.cleaned_data['last_name']
        self.object.email = form.cleaned_data['email']
        self.object.save()

        if Profile.objects.filter(user=self.object):
            profile = Perfil.objects.get(user=self.object)
            profile.phone = form.cleaned_data['phone']
            profile.save()
        return super(NationalLevelUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(NationalLevelUpdateView, self).form_invalid(form)

class StateLevelListView(ListView):
    model = StateLevel
    template_name = 'user/state.level.list.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.profile.level == 1:
            return super(StateLevelListView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_queryset(self):
        ## usuario nacioanl puede ver al nivel estadal
        if NationalLevel.objects.filter(profile=self.request.user.profile):
            national_level = NationalLevel.objects.get(profile=self.request.user.profile)
            queryset = StateLevel.objects.filter(state__country=national_level.country)
            return queryset

class StateLevelCreateView(CreateView):
    model = User
    form_class = StateLevelForm
    template_name = 'user/state.level.create.html'
    success_url = reverse_lazy('user:state_level_list')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.profile.level == 1:
            return super(StateLevelCreateView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_form_kwargs(self):
        kwargs = super(StateLevelCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.username = form.cleaned_data['username']
        self.object.first_name = form.cleaned_data['first_name']
        self.object.last_name = form.cleaned_data['last_name']
        self.object.email = form.cleaned_data['email']
        self.object.set_password(form.cleaned_data['password'])
        self.object.is_active = True
        self.object.save()

        profile = Profile.objects.create(
            phone=form.cleaned_data['phone'],
            level = 2,
            user= self.object
        )

        state = State.objects.get(pk=form.cleaned_data['state'])
        state_level = StateLevel.objects.create(
            state = state,
            profile = profile
        )

        admin, admin_email = '', ''
        if settings.ADMINS:
            admin = settings.ADMINS[0][0]
            admin_email = settings.ADMINS[0][1]

        national_level = NationalLevel.objects.get(profile=self.request.user.profile)

        sent = send_email(self.object.email, 'user/welcome.mail', EMAIL_SUBJECT, {'first_name':self.request.user.first_name,
            'last_name':self.request.user.last_name, 'email':self.request.user.email, 'phone':self.request.user.profile.phone,
            'level2':state_level.state,'username':self.object.username, 'password':form.cleaned_data['password'],
            'admin':admin, 'admin_email':admin_email, 'emailapp':settings.EMAIL_FROM, 'url':get_current_site(self.request).name,
            'level1':national_level.country
        })

        if not sent:
            logger.warning(
                str(_("Ocurrió un inconveniente al enviar por correo las credenciales del usuario [%s]") % self.object.username)
            )

        return super(StateLevelCreateView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(StateLevelCreateView, self).form_invalid(form)

class StateLevelUpdateView(UpdateView):
    model = User
    form_class = StateLevelUpdateForm
    template_name = 'user/state.level.update.html'
    success_url = reverse_lazy('base:home')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.id == self.kwargs['pk'] and self.request.user.profile.level == 2:
            return super(StateLevelUpdateView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_initial(self):
        initial_data = super(StateLevelUpdateView, self).get_initial()
        initial_data['phone'] = self.object.profile.phone
        state_level = StateLevel.objects.get(profile=self.object.profile)
        initial_data['state'] = state_level.state
        return initial_data

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.username = form.cleaned_data['username']
        self.object.first_name = form.cleaned_data['first_name']
        self.object.last_name = form.cleaned_data['last_name']
        self.object.email = form.cleaned_data['email']
        self.object.save()

        if Profile.objects.filter(user=self.object):
            profile = Profile.objects.get(user=self.object)
            profile.phone = form.cleaned_data['phone']
            profile.save()
        return super(StateLevelUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(StateLevelUpdateView, self).form_invalid(form)

class MunicipalLevelListView(ListView):
    model = MunicipalLevel
    template_name = 'user/municipal.level.list.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.profile.level == 1 or self.request.user.profile.level == 2:
            return super(MunicipalLevelListView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_queryset(self):
        ## usuario nacional puede ver al nivel municipal
        if NationalLevel.objects.filter(profile=self.request.user.profile):
            national_level = NationalLevel.objects.get(profile=self.request.user.profile)
            queryset = MunicipalLevel.objects.filter(municipality__state__country=national_level.country)
            return queryset

        ## usuario estadal puede ver al nivel municipal
        if StateLevel.objects.filter(profile=self.request.user.profile):
            state_level = StateLevel.objects.get(profile=self.request.user.profile)
            queryset = MunicipalLevel.objects.filter(municipality__state=state_level.state)
            return queryset

class MunicipalLevelCreateView(CreateView):
    model = User
    form_class = MunicipalLevelForm
    template_name = 'user/municipal.level.create.html'
    success_url = reverse_lazy('user:municipal_level_list')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.profile.level == 2:
            return super(MunicipalLevelCreateView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_form_kwargs(self):
        kwargs = super(MunicipalLevelCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.username = form.cleaned_data['username']
        self.object.first_name = form.cleaned_data['first_name']
        self.object.last_name = form.cleaned_data['last_name']
        self.object.email = form.cleaned_data['email']
        self.object.set_password(form.cleaned_data['password'])
        self.object.is_active = True
        self.object.save()

        profile = Profile.objects.create(
            phone=form.cleaned_data['phone'],
            level = 3,
            user= self.object
        )

        municipality = Municipality.objects.get(pk=form.cleaned_data['municipality'])
        municipal_level = MunicipalLevel.objects.create(
            municipality = municipality,
            profile = profile
        )

        admin, admin_email = '', ''
        if settings.ADMINS:
            admin = settings.ADMINS[0][0]
            admin_email = settings.ADMINS[0][1]

        state_level = StateLevel.objects.get(profile=self.request.user.profile)

        sent = send_email(self.object.email, 'user/welcome.mail', EMAIL_SUBJECT, {'first_name':self.request.user.first_name,
            'last_name':self.request.user.last_name, 'email':self.request.user.email, 'phone':self.request.user.profile.phone,
            'level2':municipal_level.municipality,'username':self.object.username, 'password':form.cleaned_data['password'],
            'admin':admin, 'admin_email':admin_email, 'emailapp':settings.EMAIL_FROM, 'url':get_current_site(self.request).name,
            'level1':state_level.state
        })

        if not sent:
            logger.warning(
                str(_("Ocurrió un inconveniente al enviar por correo las credenciales del usuario [%s]") % self.object.username)
            )

        return super(MunicipalLevelCreateView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(MunicipalLevelCreateView, self).form_invalid(form)

class MunicipalLevelUpdateView(UpdateView):
    model = User
    form_class = MunicipalLevelUpdateForm
    template_name = 'user/municipal.level.update.html'
    success_url = reverse_lazy('base:home')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.id == self.kwargs['pk'] and self.request.user.profile.level == 3:
            return super(MunicipalLevelUpdateView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_form_kwargs(self):
        kwargs = super(MunicipalLevelUpdateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_initial(self):
        initial_data = super(MunicipalLevelUpdateView, self).get_initial()
        initial_data['phone'] = self.object.profile.phone
        municipal_level = MunicipalLevel.objects.get(profile=self.object.profile)
        initial_data['municipality'] = municipal_level.municipality
        return initial_data

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.username = form.cleaned_data['username']
        self.object.first_name = form.cleaned_data['first_name']
        self.object.last_name = form.cleaned_data['last_name']
        self.object.email = form.cleaned_data['email']
        self.object.save()

        if Profile.objects.filter(user=self.object):
            profile = Profile.objects.get(user=self.object)
            profile.phone = form.cleaned_data['phone']
            profile.save()
        return super(MunicipalLevelUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(MunicipalLevelUpdateView, self).form_invalid(form)

class ParishLevelListView(ListView):
    model = ParishLevel
    template_name = 'user/parish.level.list.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.profile.level == 1 or self.request.user.profile.level == 2 or self.request.user.profile.level == 3:
            return super(ParishLevelListView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_queryset(self):
        ## usuario nacional puede ver al nivel parroquial
        if NationalLevel.objects.filter(profile=self.request.user.profile):
            national_level = NationalLevel.objects.get(profile=self.request.user.profile)
            queryset = ParishLevel.objects.filter(parish__municipality__state__country=national_level.country)
            return queryset

        ## usuario estadal puede ver al nivel parroquial
        if StateLevel.objects.filter(profile=self.request.user.profile):
            state_level = StateLevel.objects.get(profile=self.request.user.profile)
            queryset = ParishLevel.objects.filter(parish__municipality__state=state_level.state)
            return queryset

        ## usuario municipal puede ver al parroquial
        if MunicipalLevel.objects.filter(profile=self.request.user.profile):
            municipal_level = MunicipalLevel.objects.get(profile=self.request.user.profile)
            queryset = ParishLevel.objects.filter(parish__municipality=municipal_level.municipality)
            return queryset

class ParishLevelCreateView(CreateView):
    model = User
    form_class = ParishLevelForm
    template_name = 'user/parish.level.create.html'
    success_url = reverse_lazy('user:parish_level_list')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.profile.level == 3:
            return super(ParishLevelCreateView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_form_kwargs(self):
        kwargs = super(ParishLevelCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.username = form.cleaned_data['username']
        self.object.first_name = form.cleaned_data['first_name']
        self.object.last_name = form.cleaned_data['last_name']
        self.object.email = form.cleaned_data['email']
        self.object.set_password(form.cleaned_data['password'])
        self.object.is_active = True
        self.object.save()

        profile = Profile.objects.create(
            phone=form.cleaned_data['phone'],
            level = 4,
            user= self.object
        )

        parish = Parish.objects.get(pk=form.cleaned_data['parish'])
        parish_level = ParishLevel.objects.create(
            parish = parish,
            profile = profile
        )

        admin, admin_email = '', ''
        if settings.ADMINS:
            admin = settings.ADMINS[0][0]
            admin_email = settings.ADMINS[0][1]

        municipal_level = MunicipalLevel.objects.get(profile=self.request.user.profile)

        sent = send_email(self.object.email, 'user/welcome.mail', EMAIL_SUBJECT, {'first_name':self.request.user.first_name,
            'last_name':self.request.user.last_name, 'email':self.request.user.email, 'phone':self.request.user.profile.phone,
            'level2':parish_level.parish,'username':self.object.username, 'password':form.cleaned_data['password'],
            'admin':admin, 'admin_email':admin_email, 'emailapp':settings.EMAIL_FROM, 'url':get_current_site(self.request).name,
            'level1':municipal_level.municipality
        })

        if not sent:
            logger.warning(
                str(_("Ocurrió un inconveniente al enviar por correo las credenciales del usuario [%s]") % self.object.username)
            )

        return super(ParishLevelCreateView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(ParishLevelCreateView, self).form_invalid(form)

class ParishLevelUpdateView(UpdateView):
    model = User
    form_class = ParishLevelUpdateForm
    template_name = 'user/parish.level.update.html'
    success_url = reverse_lazy('base:home')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.id == self.kwargs['pk'] and self.request.user.profile.level == 4:
            return super(ParishLevelUpdateView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_form_kwargs(self):
        kwargs = super(ParishLevelUpdateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_initial(self):
        initial_data = super(ParishLevelUpdateView, self).get_initial()
        initial_data['phone'] = self.object.profile.phone
        parish_level = ParishLevel.objects.get(profile=self.object.profile)
        initial_data['parish'] = parish_level.parish
        return initial_data

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.username = form.cleaned_data['username']
        self.object.first_name = form.cleaned_data['first_name']
        self.object.last_name = form.cleaned_data['last_name']
        self.object.email = form.cleaned_data['email']
        self.object.save()

        if Profile.objects.filter(user=self.object):
            profile = Profile.objects.get(user=self.object)
            profile.phone = form.cleaned_data['phone']
            profile.save()
        return super(ParishLevelUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(ParishLevelUpdateView, self).form_invalid(form)

class CommunalCouncilLevelListView(ListView):
    model = CommunalCouncilLevel
    template_name = 'user/communal.council.level.list.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.profile.level == 1 or self.request.user.profile.level == 2 or self.request.user.profile.level == 3 or self.request.user.profile.level == 4:
            return super(CommunalCouncilLevelListView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_queryset(self):
        ## usuario nacional puede ver al nivel comunal
        if NationalLevel.objects.filter(profile=self.request.user.profile):
            national_level = NationalLevel.objects.get(profile=self.request.user.profile)
            queryset = CommunalCouncilLevel.objects.filter(communal_council__parish__municipality__state__country=national_level.country)
            return queryset

        ## usuario estadal puede ver al nivel comunal
        if StateLevel.objects.filter(profile=self.request.user.profile):
            state_level = StateLevel.objects.get(profile=self.request.user.profile)
            queryset = CommunalCouncilLevel.objects.filter(communal_council__parish__municipality__state=state_level.state)
            return queryset

        ## usuario municipal puede ver al comunal
        if MunicipalLevel.objects.filter(profile=self.request.user.profile):
            municipal_level = MunicipalLevel.objects.get(profile=self.request.user.profile)
            queryset = CommunalCouncilLevel.objects.filter(communal_council__parish__municipality=municipal_level.municipality)
            return queryset

        ## usuario parroquial puede ver al comunal
        if ParishLevel.objects.filter(profile=self.request.user.profile):
            parish_level = ParishLevel.objects.get(profile=self.request.user.profile)
            queryset = CommunalCouncilLevel.objects.filter(communal_council__parish=parish_level.parish)
            return queryset

class CommunalCouncilLevelCreateView(CreateView):
    model = User
    form_class = CommunalCouncilLevelForm
    template_name = 'user/communal.council.level.create.html'
    success_url = reverse_lazy('user:communal_council_level_list')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.profile.level == 4:
            return super(CommunalCouncilLevelCreateView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_form_kwargs(self):
        kwargs = super(CommunalCouncilLevelCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.username = form.cleaned_data['username']
        self.object.first_name = form.cleaned_data['first_name']
        self.object.last_name = form.cleaned_data['last_name']
        self.object.email = form.cleaned_data['email']
        self.object.set_password(form.cleaned_data['password'])
        self.object.is_active = True
        self.object.save()

        profile = Profile.objects.create(
            phone=form.cleaned_data['phone'],
            level = 5,
            user= self.object
        )

        communal_council = CommunalCouncil.objects.get(pk=form.cleaned_data['communal_council'])
        communal_council_level = CommunalCouncilLevel.objects.create(
            communal_council = communal_council,
            profile = profile
        )

        admin, admin_email = '', ''
        if settings.ADMINS:
            admin = settings.ADMINS[0][0]
            admin_email = settings.ADMINS[0][1]

        parish_level = ParishLevel.objects.get(profile=self.request.user.profile)

        sent = send_email(self.object.email, 'user/welcome.mail', EMAIL_SUBJECT, {'first_name':self.request.user.first_name,
            'last_name':self.request.user.last_name, 'email':self.request.user.email, 'phone':self.request.user.profile.phone,
            'level2':communal_council_level.communal_council,'username':self.object.username, 'password':form.cleaned_data['password'],
            'admin':admin, 'admin_email':admin_email, 'emailapp':settings.EMAIL_FROM, 'url':get_current_site(self.request).name,
            'level1':parish_level.parish
        })

        if not sent:
            logger.warning(
                str(_("Ocurrió un inconveniente al enviar por correo las credenciales del usuario [%s]") % self.object.username)
            )

        return super(CommunalCouncilLevelCreateView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(CommunalCouncilLevelCreateView, self).form_invalid(form)

class CommunalCouncilLevelUpdateView(UpdateView):
    model = User
    form_class = CommunalCouncilLevelUpdateForm
    template_name = 'user/communal.council.level.update.html'
    success_url = reverse_lazy('base:home')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.id == self.kwargs['pk'] and self.request.user.profile.level == 5:
            return super(CommunalCouncilLevelUpdateView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_form_kwargs(self):
        kwargs = super(CommunalCouncilLevelUpdateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_initial(self):
        initial_data = super(CommunalCouncilLevelUpdateView, self).get_initial()
        initial_data['phone'] = self.object.profile.phone
        communal_council_level = CommunalCouncilLevel.objects.get(profile=self.object.profile)
        initial_data['communal_council'] = communal_council_level.communal_council
        return initial_data

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.username = form.cleaned_data['username']
        self.object.first_name = form.cleaned_data['first_name']
        self.object.last_name = form.cleaned_data['last_name']
        self.object.email = form.cleaned_data['email']
        self.object.save()

        if Profile.objects.filter(user=self.object):
            profile = Profile.objects.get(user=self.object)
            profile.phone = form.cleaned_data['phone']
            profile.save()
        return super(CommunalCouncilLevelUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(CommunalCouncilLevelUpdateView, self).form_invalid(form)
