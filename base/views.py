from django.shortcuts import render
from django.views.generic import TemplateView
from usuario.models import Nacional, Estadal, Municipal, Parroquial, Comunal

# Create your views here.

class InicioView(TemplateView):
    """!
    Clase para mostrar la página de inicio según el nivel de usuario

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 26-01-2018
    @version 1.0.0
    """

    template_name = "base.template.html"

    def get_context_data(self, **kwargs):
        context = super(InicioView, self).get_context_data(**kwargs)
        perfil = self.request.user.perfil
        if perfil.nivel == 0:
            context['texto1'] = 'Bienvenido ' + str(perfil)
            context['texto2'] = 'Usuario nivel administrador. Este usuario permite registrar y eliminar \
            a cualquier usuario desde el panel administrativo'
        elif perfil.nivel == 1:
            nacional = Nacional.objects.get(perfil=perfil)
            context['texto1'] = 'Bienvenido ' + str(perfil)
            context['texto2'] = 'Usuario nivel nacional ' + str(nacional.pais) + '. Este usuario permite registrar y monitoriar a los representantes de \
            cada estado que pertenecen a dicho país'
        elif perfil.nivel == 2:
            estadal = Estadal.objects.get(perfil=perfil)
            context['texto1'] = 'Bienvenido ' + str(perfil)
            context['texto2'] = 'Usuario nivel estado ' + str(estadal.estado) + '. Este usuario permite registrar y monitoriar a los representantes de \
            cada municipio que pertenecen a dicho estado'
        elif perfil.nivel == 3:
            municipal = Municipal.objects.get(perfil=perfil)
            context['texto1'] = 'Bienvenido ' + str(perfil)
            context['texto2'] = 'Usuario nivel municipio ' + str(municipal.municipio) + '. Este usuario permite registrar y monitoriar a los representantes \
            de cada parroquia que pertenecen a dicho municipio'
        elif perfil.nivel == 4:
            parroquial = Parroquial.objects.get(perfil=perfil)
            context['texto1'] = 'Bienvenido ' + str(perfil)
            context['texto2'] = 'Usuario nivel parroquia ' + str(parroquial.parroquia) + '. Este usuario permite registrar y monitoriar a los representantes \
            de cada consejo comunal que pertenecen a dicha parroquia'
        elif perfil.nivel == 5:
            comunal = Comunal.objects.get(perfil=perfil)
            context['texto1'] = 'Bienvenido ' + str(perfil)
            context['texto2'] = 'Usuario nivel consejo comunal ' + str(comunal.consejo_comunal) + '. Este usuario permite registrar, actualizar, eliminar y listar \
            a todos los adultos mayores'
        return context

class Error403View(TemplateView):
    """!
    Clase para mostrar error de permiso

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 14-01-2018
    @version 1.0.0
    """

    template_name = "base.error.403.html"
