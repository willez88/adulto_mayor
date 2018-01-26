from django.shortcuts import render
from django.views.generic import TemplateView
from usuario.models import Estadal, Municipal, Parroquial

# Create your views here.

class InicioView(TemplateView):
    template_name = "base.template.html"

    def get_context_data(self, **kwargs):
        context = super(InicioView, self).get_context_data(**kwargs)
        perfil = self.request.user.perfil
        if perfil.nivel == 0:
            context['texto1'] = 'Bienvenido ' + str(perfil)
            context['texto2'] = 'Usuario nivel administrador. Este usuario permite registrar y eliminar \
            a cualquier usuario desde el panel administrativo'
        elif perfil.nivel == 1:
            estadal = Estadal.objects.get(perfil=perfil)
            context['texto1'] = 'Bienvenido ' + str(perfil)
            context['texto2'] = 'Usuario nivel estado ' + str(estadal.estado) + '. Este usuario permite registrar y monitoriar a los representantes de \
            cada municipio que pertenecen a dicho estado'
        elif perfil.nivel == 2:
            municipal = Municipal.objects.get(perfil=perfil)
            context['texto1'] = 'Bienvenido ' + str(perfil)
            context['texto2'] = 'Usuario nivel municipio ' + str(municipal.municipio) + '. Este usuario permite registrar y monitoriar a los representantes \
            de cada parroquia que pertenecen a dicho municipio'
        elif perfil.nivel == 3:
            parroquial = Parroquial.objects.get(perfil=perfil)
            context['dato'] = parroquial.parroquia
        return context

class Error403View(TemplateView):
    template_name = "base.error.403.html"
