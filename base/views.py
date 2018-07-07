from django.shortcuts import render
from django.views.generic import TemplateView
from user.models import NationalLevel, StateLevel, MunicipalLevel, ParishLevel, CommunalCouncilLevel

class HomeView(TemplateView):
    """!
    Clase para mostrar la página de inicio según el nivel de usuario

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 26-01-2018
    @version 1.0.0
    """

    template_name = "base/base.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        profile = self.request.user.profile
        if profile.level == 0:
            context['texto1'] = 'Bienvenido ' + str(profile)
            context['texto2'] = 'Usuario nivel administrador. Este usuario permite registrar y eliminar \
            a cualquier usuario desde el panel administrativo'
        elif profile.level == 1:
            national_level = NationalLevel.objects.get(profile=profile)
            context['texto1'] = 'Bienvenido ' + str(profile)
            context['texto2'] = 'Usuario nivel nacional ' + str(national_level.country) + '. Este usuario permite registrar y monitoriar a los representantes de \
            cada estado que pertenecen a dicho país'
        elif profile.level == 2:
            state_level = StateLevel.objects.get(profile=profile)
            context['texto1'] = 'Bienvenido ' + str(profile)
            context['texto2'] = 'Usuario nivel estado ' + str(state_level.state) + '. Este usuario permite registrar y monitoriar a los representantes de \
            cada municipio que pertenecen a dicho estado'
        elif profile.level == 3:
            municipal_level = MunicipalLevel.objects.get(profile=profile)
            context['texto1'] = 'Bienvenido ' + str(profile)
            context['texto2'] = 'Usuario nivel municipio ' + str(municipal_level.municipality) + '. Este usuario permite registrar y monitoriar a los representantes \
            de cada parroquia que pertenecen a dicho municipio'
        elif profile.level == 4:
            parish_level = ParishLevel.objects.get(profile=profile)
            context['texto1'] = 'Bienvenido ' + str(profile)
            context['texto2'] = 'Usuario nivel parroquia ' + str(parish_level.parish) + '. Este usuario permite registrar y monitoriar a los representantes \
            de cada consejo comunal que pertenecen a dicha parroquia'
        elif profile.level == 5:
            communal_council_level = CommunalCouncilLevel.objects.get(profile=profile)
            context['texto1'] = 'Bienvenido ' + str(profile)
            context['texto2'] = 'Usuario nivel consejo comunal ' + str(communal_council_level.communal_council) + '. Este usuario permite registrar, actualizar, eliminar y listar \
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

    template_name = "base/error.403.html"
