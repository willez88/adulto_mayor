from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import (
    NacionalUpdateForm, EstadalForm, EstadalUpdateForm, MunicipalForm, ParroquialForm, MunicipalUpdateForm,
    ParroquialUpdateForm, ComunalForm, ComunalUpdateForm
)
from .models import Perfil, Nacional, Estadal, Municipal, Parroquial, Comunal
from django.contrib.auth.models import User
from base.models import Estado, Municipio, Parroquia, ConsejoComunal
from django.conf import settings
from base.constant import EMAIL_SUBJECT_REGISTRO
from base.functions import enviar_correo
from django.utils.translation import ugettext_lazy as _
import logging
logger = logging.getLogger("usuario")

# Create your views here.

class NacionalUpdate(UpdateView):
    model = User
    form_class = NacionalUpdateForm
    template_name = "usuario.nacional.actualizar.html"
    success_url = reverse_lazy('inicio')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.id == self.kwargs['pk'] and self.request.user.perfil.nivel == 1:
            return super(NacionalUpdate, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('error_403')

    def get_initial(self):
        datos_iniciales = super(NacionalUpdate, self).get_initial()
        perfil = Perfil.objects.get(user=self.object)
        datos_iniciales['telefono'] = perfil.telefono
        nacional = Nacional.objects.get(perfil=perfil)
        datos_iniciales['pais'] = nacional.pais
        return datos_iniciales

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.username = form.cleaned_data['username']
        self.object.first_name = form.cleaned_data['first_name']
        self.object.last_name = form.cleaned_data['last_name']
        self.object.email = form.cleaned_data['email']
        self.object.save()

        if Perfil.objects.filter(user=self.object):
            perfil = Perfil.objects.get(user=self.object)
            perfil.telefono = form.cleaned_data['telefono']
            perfil.save()
        return super(NacionalUpdate, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(NacionalUpdate, self).form_invalid(form)

class EstadalList(ListView):
    model = Estadal
    template_name = "usuario.estadal.listar.html"

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.perfil.nivel == 1:
            return super(EstadalList, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('error_403')

    def get_queryset(self):
        ## usuario nacioanl puede ver al nivel estadal
        if Nacional.objects.filter(perfil=self.request.user.perfil):
            nacional = Nacional.objects.get(perfil=self.request.user.perfil)
            queryset = Estadal.objects.filter(estado__pais=nacional.pais)
            return queryset

class EstadalCreate(CreateView):
    model = User
    form_class = EstadalForm
    template_name = "usuario.estadal.registrar.html"
    success_url = reverse_lazy('estadal_listar')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.perfil.nivel == 1:
            return super(EstadalCreate, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('error_403')

    def get_form_kwargs(self):
        kwargs = super(EstadalCreate, self).get_form_kwargs()
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

        user = User.objects.get(username=self.object.username)
        perfil = Perfil.objects.create(
            telefono=form.cleaned_data['telefono'],
            nivel = 2,
            user= user
        )

        estado = Estado.objects.get(pk=form.cleaned_data['estado'])
        Estadal.objects.create(
            estado = estado,
            perfil = perfil
        )

        admin, admin_email = '', ''
        if settings.ADMINS:
            admin = settings.ADMINS[0][0]
            admin_email = settings.ADMINS[0][1]

        enviado = enviar_correo(self.object.email, 'usuario.bienvenida.mail', EMAIL_SUBJECT_REGISTRO, {'nivel':'Nacional','nombre':self.request.user.first_name,
            'apellido':self.request.user.last_name, 'correo':self.request.user.email, 'username':self.object.username, 'clave':form.cleaned_data['password'],
            'admin':admin, 'admin_email':admin_email, 'emailapp':settings.EMAIL_FROM
        })

        if not enviado:
            logger.warning(
                str(_("Ocurrió un inconveniente al enviar por correo las credenciales del usuario [%s]") % self.object.username)
            )

        return super(EstadalCreate, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(EstadalCreate, self).form_invalid(form)

class EstadalUpdate(UpdateView):
    model = User
    form_class = EstadalUpdateForm
    template_name = "usuario.estadal.actualizar.html"
    success_url = reverse_lazy('inicio')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.id == self.kwargs['pk'] and self.request.user.perfil.nivel == 2:
            return super(EstadalUpdate, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('error_403')

    def get_initial(self):
        datos_iniciales = super(EstadalUpdate, self).get_initial()
        perfil = Perfil.objects.get(user=self.object)
        datos_iniciales['telefono'] = perfil.telefono
        estadal = Estadal.objects.get(perfil=perfil)
        datos_iniciales['estado'] = estadal.estado
        return datos_iniciales

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.username = form.cleaned_data['username']
        self.object.first_name = form.cleaned_data['first_name']
        self.object.last_name = form.cleaned_data['last_name']
        self.object.email = form.cleaned_data['email']
        self.object.save()

        if Perfil.objects.filter(user=self.object):
            perfil = Perfil.objects.get(user=self.object)
            perfil.telefono = form.cleaned_data['telefono']
            perfil.save()
        return super(EstadalUpdate, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(EstadalUpdate, self).form_invalid(form)

class MunicipalList(ListView):
    model = Municipal
    template_name = "usuario.municipal.listar.html"

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.perfil.nivel == 1 or self.request.user.perfil.nivel == 2:
            return super(MunicipalList, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('error_403')

    def get_queryset(self):
        ## usuario nacional puede ver al nivel municipal
        if Nacional.objects.filter(perfil=self.request.user.perfil):
            nacional = Nacional.objects.get(perfil=self.request.user.perfil)
            queryset = Municipal.objects.filter(municipio__estado__pais=nacional.pais)
            return queryset

        ## usuario estadal puede ver al nivel municipal
        if Estadal.objects.filter(perfil=self.request.user.perfil):
            estadal = Estadal.objects.get(perfil=self.request.user.perfil)
            queryset = Municipal.objects.filter(municipio__estado=estadal.estado)
            return queryset

class MunicipalCreate(CreateView):
    model = User
    form_class = MunicipalForm
    template_name = "usuario.municipal.registrar.html"
    success_url = reverse_lazy('municipal_listar')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.perfil.nivel == 2:
            return super(MunicipalCreate, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('error_403')

    def get_form_kwargs(self):
        kwargs = super(MunicipalCreate, self).get_form_kwargs()
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

        user = User.objects.get(username=self.object.username)
        perfil = Perfil.objects.create(
            telefono=form.cleaned_data['telefono'],
            nivel = 3,
            user= user
        )

        municipio = Municipio.objects.get(pk=form.cleaned_data['municipio'])
        Municipal.objects.create(
            municipio = municipio,
            perfil = perfil
        )

        admin, admin_email = '', ''
        if settings.ADMINS:
            admin = settings.ADMINS[0][0]
            admin_email = settings.ADMINS[0][1]

        enviado = enviar_correo(self.object.email, 'usuario.bienvenida.mail', EMAIL_SUBJECT_REGISTRO, {'nivel':'Estadal','nombre':self.request.user.first_name,
            'apellido':self.request.user.last_name, 'correo':self.request.user.email, 'username':self.object.username, 'clave':form.cleaned_data['password'],
            'admin':admin, 'admin_email':admin_email, 'emailapp':settings.EMAIL_FROM
        })

        if not enviado:
            logger.warning(
                str(_("Ocurrió un inconveniente al enviar por correo las credenciales del usuario [%s]") % self.object.username)
            )

        return super(MunicipalCreate, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(MunicipalCreate, self).form_invalid(form)

class MunicipalUpdate(UpdateView):
    model = User
    form_class = MunicipalUpdateForm
    template_name = "usuario.municipal.actualizar.html"
    success_url = reverse_lazy('inicio')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.id == self.kwargs['pk'] and self.request.user.perfil.nivel == 3:
            return super(MunicipalUpdate, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('error_403')

    def get_form_kwargs(self):
        kwargs = super(MunicipalUpdate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_initial(self):
        datos_iniciales = super(MunicipalUpdate, self).get_initial()
        perfil = Perfil.objects.get(user=self.object)
        datos_iniciales['telefono'] = perfil.telefono
        municipal = Municipal.objects.get(perfil=perfil)
        datos_iniciales['municipio'] = municipal.municipio
        return datos_iniciales

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.username = form.cleaned_data['username']
        self.object.first_name = form.cleaned_data['first_name']
        self.object.last_name = form.cleaned_data['last_name']
        self.object.email = form.cleaned_data['email']
        self.object.save()

        if Perfil.objects.filter(user=self.object):
            perfil = Perfil.objects.get(user=self.object)
            perfil.telefono = form.cleaned_data['telefono']
            perfil.save()
        return super(MunicipalUpdate, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(MunicipalUpdate, self).form_invalid(form)

class ParroquialList(ListView):
    model = Parroquial
    template_name = "usuario.parroquial.listar.html"

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.perfil.nivel == 1 or self.request.user.perfil.nivel == 2 or self.request.user.perfil.nivel == 3:
            return super(ParroquialList, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('error_403')

    def get_queryset(self):
        ## usuario nacional puede ver al nivel parroquial
        if Nacional.objects.filter(perfil=self.request.user.perfil):
            nacional = Nacional.objects.get(perfil=self.request.user.perfil)
            queryset = Parroquial.objects.filter(parroquia__municipio__estado__pais=nacional.pais)
            return queryset

        ## usuario estadal puede ver al nivel parroquial
        if Estadal.objects.filter(perfil=self.request.user.perfil):
            estadal = Estadal.objects.get(perfil=self.request.user.perfil)
            queryset = Parroquial.objects.filter(parroquia__municipio__estado=estadal.estado)
            return queryset

        ## usuario municipal puede ver al parroquial
        if Municipal.objects.filter(perfil=self.request.user.perfil):
            municipal = Municipal.objects.get(perfil=self.request.user.perfil)
            queryset = Parroquial.objects.filter(parroquia__municipio=municipal.municipio)
            return queryset

class ParroquialCreate(CreateView):
    model = User
    form_class = ParroquialForm
    template_name = "usuario.parroquial.registrar.html"
    success_url = reverse_lazy('parroquial_listar')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.perfil.nivel == 3:
            return super(ParroquialCreate, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('error_403')

    def get_form_kwargs(self):
        kwargs = super(ParroquialCreate, self).get_form_kwargs()
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

        user = User.objects.get(username=self.object.username)
        perfil = Perfil.objects.create(
            telefono=form.cleaned_data['telefono'],
            nivel = 4,
            user= user
        )

        parroquia = Parroquia.objects.get(pk=form.cleaned_data['parroquia'])
        Parroquial.objects.create(
            parroquia = parroquia,
            perfil = perfil
        )

        admin, admin_email = '', ''
        if settings.ADMINS:
            admin = settings.ADMINS[0][0]
            admin_email = settings.ADMINS[0][1]

        enviado = enviar_correo(self.object.email, 'usuario.bienvenida.mail', EMAIL_SUBJECT_REGISTRO, {'nivel':'Municipal','nombre':self.request.user.first_name,
            'apellido':self.request.user.last_name, 'correo':self.request.user.email, 'username':self.object.username, 'clave':form.cleaned_data['password'],
            'admin':admin, 'admin_email':admin_email, 'emailapp':settings.EMAIL_FROM
        })

        if not enviado:
            logger.warning(
                str(_("Ocurrió un inconveniente al enviar por correo las credenciales del usuario [%s]") % self.object.username)
            )

        return super(ParroquialCreate, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(ParroquialCreate, self).form_invalid(form)

class ParroquialUpdate(UpdateView):
    model = User
    form_class = ParroquialUpdateForm
    template_name = "usuario.parroquial.actualizar.html"
    success_url = reverse_lazy('inicio')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.id == self.kwargs['pk'] and self.request.user.perfil.nivel == 4:
            return super(ParroquialUpdate, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('error_403')

    def get_form_kwargs(self):
        kwargs = super(ParroquialUpdate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_initial(self):
        datos_iniciales = super(ParroquialUpdate, self).get_initial()
        perfil = Perfil.objects.get(user=self.object)
        datos_iniciales['telefono'] = perfil.telefono
        parroquial = Parroquial.objects.get(perfil=perfil)
        datos_iniciales['parroquia'] = parroquial.parroquia
        return datos_iniciales

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.username = form.cleaned_data['username']
        self.object.first_name = form.cleaned_data['first_name']
        self.object.last_name = form.cleaned_data['last_name']
        self.object.email = form.cleaned_data['email']
        self.object.save()

        if Perfil.objects.filter(user=self.object):
            perfil = Perfil.objects.get(user=self.object)
            perfil.telefono = form.cleaned_data['telefono']
            perfil.save()
        return super(ParroquialUpdate, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(ParroquialUpdate, self).form_invalid(form)

class ComunalList(ListView):
    model = Comunal
    template_name = "usuario.comunal.listar.html"

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.perfil.nivel == 1 or self.request.user.perfil.nivel == 2 or self.request.user.perfil.nivel == 3 or self.request.user.perfil.nivel == 4:
            return super(ComunalList, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('error_403')

    def get_queryset(self):
        ## usuario nacional puede ver al nivel comunal
        if Nacional.objects.filter(perfil=self.request.user.perfil):
            nacional = Nacional.objects.get(perfil=self.request.user.perfil)
            queryset = Comunal.objects.filter(consejo_comunal__parroquia__municipio__estado__pais=nacional.pais)
            return queryset

        ## usuario estadal puede ver al nivel comunal
        if Estadal.objects.filter(perfil=self.request.user.perfil):
            estadal = Estadal.objects.get(perfil=self.request.user.perfil)
            queryset = Comunal.objects.filter(consejo_comunal__parroquia__municipio__estado=estadal.estado)
            return queryset

        ## usuario municipal puede ver al comunal
        if Municipal.objects.filter(perfil=self.request.user.perfil):
            municipal = Municipal.objects.get(perfil=self.request.user.perfil)
            queryset = Comunal.objects.filter(consejo_comunal__parroquia__municipio=municipal.municipio)
            return queryset

        ## usuario parroquial puede ver al comunal
        if Parroquial.objects.filter(perfil=self.request.user.perfil):
            parroquial = Parroquial.objects.get(perfil=self.request.user.perfil)
            queryset = Comunal.objects.filter(consejo_comunal__parroquia=parroquial.parroquia)
            return queryset

class ComunalCreate(CreateView):
    model = User
    form_class = ComunalForm
    template_name = "usuario.comunal.registrar.html"
    success_url = reverse_lazy('comunal_listar')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.perfil.nivel == 4:
            return super(ComunalCreate, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('error_403')

    def get_form_kwargs(self):
        kwargs = super(ComunalCreate, self).get_form_kwargs()
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

        user = User.objects.get(username=self.object.username)
        perfil = Perfil.objects.create(
            telefono=form.cleaned_data['telefono'],
            nivel = 5,
            user= user
        )

        consejo_comunal = ConsejoComunal.objects.get(pk=form.cleaned_data['consejo_comunal'])
        Comunal.objects.create(
            consejo_comunal = consejo_comunal,
            perfil = perfil
        )

        admin, admin_email = '', ''
        if settings.ADMINS:
            admin = settings.ADMINS[0][0]
            admin_email = settings.ADMINS[0][1]

        enviado = enviar_correo(self.object.email, 'usuario.bienvenida.mail', EMAIL_SUBJECT_REGISTRO, {'nivel':'Parroquial','nombre':self.request.user.first_name,
            'apellido':self.request.user.last_name, 'correo':self.request.user.email, 'username':self.object.username, 'clave':form.cleaned_data['password'],
            'admin':admin, 'admin_email':admin_email, 'emailapp':settings.EMAIL_FROM
        })

        if not enviado:
            logger.warning(
                str(_("Ocurrió un inconveniente al enviar por correo las credenciales del usuario [%s]") % self.object.username)
            )

        return super(ComunalCreate, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(ComunalCreate, self).form_invalid(form)

class ComunalUpdate(UpdateView):
    model = User
    form_class = ComunalUpdateForm
    template_name = "usuario.comunal.actualizar.html"
    success_url = reverse_lazy('inicio')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.id == self.kwargs['pk'] and self.request.user.perfil.nivel == 5:
            return super(ComunalUpdate, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('error_403')

    def get_form_kwargs(self):
        kwargs = super(ComunalUpdate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_initial(self):
        datos_iniciales = super(ComunalUpdate, self).get_initial()
        perfil = Perfil.objects.get(user=self.object)
        datos_iniciales['telefono'] = perfil.telefono
        comunal = Comunal.objects.get(perfil=perfil)
        datos_iniciales['consejo_comunal'] = comunal.consejo_comunal
        return datos_iniciales

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.username = form.cleaned_data['username']
        self.object.first_name = form.cleaned_data['first_name']
        self.object.last_name = form.cleaned_data['last_name']
        self.object.email = form.cleaned_data['email']
        self.object.save()

        if Perfil.objects.filter(user=self.object):
            perfil = Perfil.objects.get(user=self.object)
            perfil.telefono = form.cleaned_data['telefono']
            perfil.save()
        return super(ComunalUpdate, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(ComunalUpdate, self).form_invalid(form)
