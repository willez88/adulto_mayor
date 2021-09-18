import logging

from base.constant import EMAIL_SUBJECT
from base.functions import send_email
from base.models import CommunalCouncil, Municipality, Parish, State
from django.conf import settings
from django.contrib.auth.models import Group, User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from .forms import (
    CommunalCouncilLevelForm, CommunalCouncilLevelUpdateForm,
    MunicipalLevelForm, MunicipalLevelUpdateForm, NationalLevelUpdateForm,
    ParishLevelForm, ParishLevelUpdateForm, StateLevelForm,
    StateLevelUpdateForm,
)
from .models import (
    CommunalCouncilLevel, MunicipalLevel, NationalLevel, ParishLevel, Profile,
    StateLevel,
)

logger = logging.getLogger('user')


class NationalLevelUpdateView(UpdateView):
    model = Profile
    form_class = NationalLevelUpdateForm
    template_name = 'user/national.level.update.html'
    success_url = reverse_lazy('base:home')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.id == self.kwargs['pk'] and\
                self.request.user.groups.filter(name='Nivel Nacional'):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_initial(self):
        initial_data = super().get_initial()
        profile = self.request.user.profile
        initial_data['username'] = profile.user.username
        initial_data['first_name'] = profile.user.first_name
        initial_data['last_name'] = profile.user.last_name
        initial_data['email'] = profile.user.email
        national_level = NationalLevel.objects.get(profile=profile)
        initial_data['country'] = national_level.country
        return initial_data

    def form_valid(self, form):
        if User.objects.filter(username=self.object.user.username):
            user = User.objects.get(username=self.object.user.username)
            user.username = form.cleaned_data['username']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()

        self.object = form.save(commit=False)
        self.object.phone = form.cleaned_data['phone']
        self.object.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


class StateLevelListView(ListView):
    model = StateLevel
    template_name = 'user/state.level.list.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.groups.filter(name='Nivel Nacional'):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_queryset(self):
        # usuario nacional puede ver al nivel estadal
        if NationalLevel.objects.filter(profile=self.request.user.profile):
            national_level = NationalLevel.objects.get(
                profile=self.request.user.profile
            )
            queryset = StateLevel.objects.filter(
                state__country=national_level.country
            )
            return queryset


class StateLevelCreateView(CreateView):
    model = User
    form_class = StateLevelForm
    template_name = 'user/state.level.create.html'
    success_url = reverse_lazy('user:state_level_list')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.groups.filter(name='Nivel Nacional'):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
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
        self.object.groups.add(Group.objects.get(name='Nivel Estadal'))
        profile = Profile.objects.create(
            phone=form.cleaned_data['phone'],
            user=self.object
        )
        state = State.objects.get(pk=form.cleaned_data['state'])
        state_level = StateLevel.objects.create(
            state=state,
            profile=profile
        )
        admin, admin_email = '', ''
        if settings.ADMINS:
            admin = settings.ADMINS[0][0]
            admin_email = settings.ADMINS[0][1]

        national_level = NationalLevel.objects.get(
            profile=self.request.user.profile
        )
        sent = send_email(
            self.object.email, 'user/welcome.mail', EMAIL_SUBJECT,
            {
                'first_name': self.request.user.first_name,
                'last_name': self.request.user.last_name,
                'email': self.request.user.email,
                'phone': self.request.user.profile.phone,
                'level2': state_level.state, 'username': self.object.username,
                'password': form.cleaned_data['password'],
                'admin': admin, 'admin_email': admin_email,
                'emailapp': settings.EMAIL_HOST_USER,
                'url': get_current_site(self.request).name,
                'level1': national_level.country
            }
        )

        if not sent:
            logger.warning(
                str('Ocurrió un inconveniente al enviar por correo las \
                    credenciales del usuario [%s]') % self.object.username
            )

        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


class StateLevelUpdateView(UpdateView):
    model = Profile
    form_class = StateLevelUpdateForm
    template_name = 'user/state.level.update.html'
    success_url = reverse_lazy('base:home')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.id == self.kwargs['pk'] and\
                self.request.user.groups.filter(name='Nivel Estadal'):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_initial(self):
        initial_data = super().get_initial()
        profile = self.request.user.profile
        initial_data['username'] = profile.user.username
        initial_data['first_name'] = profile.user.first_name
        initial_data['last_name'] = profile.user.last_name
        initial_data['email'] = profile.user.email
        state_level = StateLevel.objects.get(profile=profile)
        initial_data['state'] = state_level.state
        return initial_data

    def form_valid(self, form):
        if User.objects.filter(username=self.object.user.username):
            user = User.objects.get(username=self.object.user.username)
            user.username = form.cleaned_data['username']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()

        self.object = form.save(commit=False)
        self.object.phone = form.cleaned_data['phone']
        self.object.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


class MunicipalLevelListView(ListView):
    model = MunicipalLevel
    template_name = 'user/municipal.level.list.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.groups.filter(name='Nivel Nacional') or\
                self.request.user.groups.filter(name='Nivel Estadal'):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_queryset(self):
        # usuario nacional puede ver al nivel municipal
        if NationalLevel.objects.filter(profile=self.request.user.profile):
            national_level = NationalLevel.objects.get(
                profile=self.request.user.profile
            )
            queryset = MunicipalLevel.objects.filter(
                municipality__state__country=national_level.country
            )
            return queryset

        # usuario estadal puede ver al nivel municipal
        if StateLevel.objects.filter(profile=self.request.user.profile):
            state_level = StateLevel.objects.get(
                profile=self.request.user.profile
            )
            queryset = MunicipalLevel.objects.filter(
                municipality__state=state_level.state
            )
            return queryset


class MunicipalLevelCreateView(CreateView):
    model = User
    form_class = MunicipalLevelForm
    template_name = 'user/municipal.level.create.html'
    success_url = reverse_lazy('user:municipal_level_list')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.groups.filter(name='Nivel Estadal'):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
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
        self.object.groups.add(Group.objects.get(name='Nivel Municipal'))

        profile = Profile.objects.create(
            phone=form.cleaned_data['phone'],
            user=self.object
        )

        municipality = Municipality.objects.get(
            pk=form.cleaned_data['municipality']
        )
        municipal_level = MunicipalLevel.objects.create(
            municipality=municipality,
            profile=profile
        )

        admin, admin_email = '', ''
        if settings.ADMINS:
            admin = settings.ADMINS[0][0]
            admin_email = settings.ADMINS[0][1]

        state_level = StateLevel.objects.get(profile=self.request.user.profile)

        sent = send_email(
            self.object.email, 'user/welcome.mail', EMAIL_SUBJECT,
            {
                'first_name': self.request.user.first_name,
                'last_name': self.request.user.last_name,
                'email': self.request.user.email,
                'phone': self.request.user.profile.phone,
                'level2': municipal_level.municipality,
                'username': self.object.username,
                'password': form.cleaned_data['password'],
                'admin': admin, 'admin_email': admin_email,
                'emailapp': settings.EMAIL_HOST_USER,
                'url': get_current_site(self.request).name,
                'level1': state_level.state
            }
        )

        if not sent:
            logger.warning(
                str('Ocurrió un inconveniente al enviar por correo las \
                    credenciales del usuario [%s]' % self.object.username)
            )

        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


class MunicipalLevelUpdateView(UpdateView):
    model = Profile
    form_class = MunicipalLevelUpdateForm
    template_name = 'user/municipal.level.update.html'
    success_url = reverse_lazy('base:home')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.id == self.kwargs['pk'] and\
                self.request.user.groups.filter(name='Nivel Municipal'):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_initial(self):
        initial_data = super().get_initial()
        profile = self.request.user.profile
        initial_data['username'] = profile.user.username
        initial_data['first_name'] = profile.user.first_name
        initial_data['last_name'] = profile.user.last_name
        initial_data['email'] = profile.user.email
        municipal_level = MunicipalLevel.objects.get(profile=profile)
        initial_data['municipality'] = municipal_level.municipality
        return initial_data

    def form_valid(self, form):
        if User.objects.filter(username=self.object.user.username):
            user = User.objects.get(username=self.object.user.username)
            user.username = form.cleaned_data['username']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()

        self.object = form.save(commit=False)
        self.object.phone = form.cleaned_data['phone']
        self.object.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


class ParishLevelListView(ListView):
    model = ParishLevel
    template_name = 'user/parish.level.list.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.groups.filter(name='Nivel Nacional') or\
            self.request.user.groups.filter(name='Nivel Estadal') or\
                self.request.user.groups.filter(name='Nivel Municipal'):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_queryset(self):
        # usuario nacional puede ver al nivel parroquial
        if NationalLevel.objects.filter(profile=self.request.user.profile):
            national_level = NationalLevel.objects.get(
                profile=self.request.user.profile
            )
            queryset = ParishLevel.objects.filter(
                parish__municipality__state__country=national_level.country
            )
            return queryset

        # usuario estadal puede ver al nivel parroquial
        if StateLevel.objects.filter(profile=self.request.user.profile):
            state_level = StateLevel.objects.get(
                profile=self.request.user.profile
            )
            queryset = ParishLevel.objects.filter(
                parish__municipality__state=state_level.state
            )
            return queryset

        # usuario municipal puede ver al parroquial
        if MunicipalLevel.objects.filter(profile=self.request.user.profile):
            municipal_level = MunicipalLevel.objects.get(
                profile=self.request.user.profile
            )
            queryset = ParishLevel.objects.filter(
                parish__municipality=municipal_level.municipality
            )
            return queryset


class ParishLevelCreateView(CreateView):
    model = User
    form_class = ParishLevelForm
    template_name = 'user/parish.level.create.html'
    success_url = reverse_lazy('user:parish_level_list')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.groups.filter(name='Nivel Municipal'):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
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
        self.object.groups.add(Group.objects.get(name='Nivel Parroquial'))

        profile = Profile.objects.create(
            phone=form.cleaned_data['phone'],
            user=self.object
        )

        parish = Parish.objects.get(pk=form.cleaned_data['parish'])
        parish_level = ParishLevel.objects.create(
            parish=parish,
            profile=profile
        )

        admin, admin_email = '', ''
        if settings.ADMINS:
            admin = settings.ADMINS[0][0]
            admin_email = settings.ADMINS[0][1]

        municipal_level = MunicipalLevel.objects.get(
            profile=self.request.user.profile
        )

        sent = send_email(
            self.object.email, 'user/welcome.mail', EMAIL_SUBJECT,
            {
                'first_name': self.request.user.first_name,
                'last_name': self.request.user.last_name,
                'email': self.request.user.email,
                'phone': self.request.user.profile.phone,
                'level2': parish_level.parish,
                'username': self.object.username,
                'password': form.cleaned_data['password'],
                'admin': admin, 'admin_email': admin_email,
                'emailapp': settings.EMAIL_HOST_USER,
                'url': get_current_site(self.request).name,
                'level1': municipal_level.municipality
            }
        )

        if not sent:
            logger.warning(
                str('Ocurrió un inconveniente al enviar por correo las \
                    credenciales del usuario [%s]' % self.object.username)
            )

        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


class ParishLevelUpdateView(UpdateView):
    model = Profile
    form_class = ParishLevelUpdateForm
    template_name = 'user/parish.level.update.html'
    success_url = reverse_lazy('base:home')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.id == self.kwargs['pk'] and\
                self.request.user.groups.filter(name='Nivel Parroquial'):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_initial(self):
        initial_data = super().get_initial()
        profile = self.request.user.profile
        initial_data['username'] = profile.user.username
        initial_data['first_name'] = profile.user.first_name
        initial_data['last_name'] = profile.user.last_name
        initial_data['email'] = profile.user.email
        parish_level = ParishLevel.objects.get(profile=profile)
        initial_data['parish'] = parish_level.parish
        return initial_data

    def form_valid(self, form):
        if User.objects.filter(username=self.object.user.username):
            user = User.objects.get(username=self.object.user.username)
            user.username = form.cleaned_data['username']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()

        self.object = form.save(commit=False)
        self.object.phone = form.cleaned_data['phone']
        self.object.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


class CommunalCouncilLevelListView(ListView):
    model = CommunalCouncilLevel
    template_name = 'user/communal.council.level.list.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.groups.filter(name='Nivel Nacional') or\
            self.request.user.groups.filter(name='Nivel Estadal') or\
            self.request.user.groups.filter(name='Nivel Municipal') or\
                self.request.user.groups.filter(name='Nivel Parroquial'):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_queryset(self):
        # usuario nacional puede ver al nivel comunal
        if NationalLevel.objects.filter(profile=self.request.user.profile):
            national_level = NationalLevel.objects.get(
                profile=self.request.user.profile
            )
            nl = national_level.country
            queryset = CommunalCouncilLevel.objects.filter(
                communal_council__parish__municipality__state__country=nl
            )
            return queryset

        # usuario estadal puede ver al nivel comunal
        if StateLevel.objects.filter(profile=self.request.user.profile):
            state_level = StateLevel.objects.get(
                profile=self.request.user.profile
            )
            queryset = CommunalCouncilLevel.objects.filter(
                communal_council__parish__municipality__state=state_level.state
            )
            return queryset

        # usuario municipal puede ver al comunal
        if MunicipalLevel.objects.filter(profile=self.request.user.profile):
            municipal_level = MunicipalLevel.objects.get(
                profile=self.request.user.profile
            )
            ml = municipal_level.municipality
            queryset = CommunalCouncilLevel.objects.filter(
                communal_council__parish__municipality=ml
            )
            return queryset

        # usuario parroquial puede ver al comunal
        if ParishLevel.objects.filter(profile=self.request.user.profile):
            parish_level = ParishLevel.objects.get(
                profile=self.request.user.profile
            )
            queryset = CommunalCouncilLevel.objects.filter(
                communal_council__parish=parish_level.parish
            )
            return queryset


class CommunalCouncilLevelCreateView(CreateView):
    model = User
    form_class = CommunalCouncilLevelForm
    template_name = 'user/communal.council.level.create.html'
    success_url = reverse_lazy('user:communal_council_level_list')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.groups.filter(name='Nivel Parroquial'):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
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
        self.object.groups.add(Group.objects.get(name='Nivel Comunal'))

        profile = Profile.objects.create(
            phone=form.cleaned_data['phone'],
            user=self.object
        )

        communal_council = CommunalCouncil.objects.get(
            pk=form.cleaned_data['communal_council']
        )
        communal_council_level = CommunalCouncilLevel.objects.create(
            communal_council=communal_council,
            profile=profile
        )

        admin, admin_email = '', ''
        if settings.ADMINS:
            admin = settings.ADMINS[0][0]
            admin_email = settings.ADMINS[0][1]

        parish_level = ParishLevel.objects.get(
            profile=self.request.user.profile
        )

        sent = send_email(
            self.object.email, 'user/welcome.mail', EMAIL_SUBJECT,
            {
                'first_name': self.request.user.first_name,
                'last_name': self.request.user.last_name,
                'email': self.request.user.email,
                'phone': self.request.user.profile.phone,
                'level2': communal_council_level.communal_council,
                'username': self.object.username,
                'password': form.cleaned_data['password'],
                'admin': admin, 'admin_email': admin_email,
                'emailapp': settings.EMAIL_HOST_USER,
                'url': get_current_site(self.request).name,
                'level1': parish_level.parish
            }
        )

        if not sent:
            logger.warning(
                str('Ocurrió un inconveniente al enviar por correo las \
                    credenciales del usuario [%s]' % self.object.username)
            )

        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


class CommunalCouncilLevelUpdateView(UpdateView):
    model = Profile
    form_class = CommunalCouncilLevelUpdateForm
    template_name = 'user/communal.council.level.update.html'
    success_url = reverse_lazy('base:home')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.id == self.kwargs['pk'] and\
                self.request.user.groups.filter(name='Nivel Comunal'):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('base:error_403')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_initial(self):
        initial_data = super().get_initial()
        profile = self.request.user.profile
        initial_data['username'] = profile.user.username
        initial_data['first_name'] = profile.user.first_name
        initial_data['last_name'] = profile.user.last_name
        initial_data['email'] = profile.user.email
        communal_council_level = CommunalCouncilLevel.objects.get(
            profile=profile
        )
        initial_data[
            'communal_council'
        ] = communal_council_level.communal_council
        return initial_data

    def form_valid(self, form):
        if User.objects.filter(username=self.object.user.username):
            user = User.objects.get(username=self.object.user.username)
            user.username = form.cleaned_data['username']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()

        self.object = form.save(commit=False)
        self.object.phone = form.cleaned_data['phone']
        self.object.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)
