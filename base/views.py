from django.views.generic import TemplateView
from user.models import (
    CommunalCouncilLevel, MunicipalLevel, NationalLevel, ParishLevel,
    StateLevel,
)


class HomeTemplateView(TemplateView):
    """!
    Clase para mostrar la página de inicio según el nivel de usuario

    @author William Páez <paez.william8@gmail.com>
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    template_name = 'base/base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.request.user.profile
        if self.request.user.groups.filter(name='Administrador'):
            context['text1'] = 'Bienvenido ' + str(profile)
            context['text2'] = 'Usuario nivel administrador. Este usuario \
                permite registrar y eliminar a cualquier usuario desde el \
                panel administrativo'
        elif self.request.user.groups.filter(name='Nivel Nacional'):
            national_level = NationalLevel.objects.get(profile=profile)
            context['text1'] = 'Bienvenido ' + str(profile)
            context['text2'] = 'Usuario nivel nacional ' +\
                str(national_level.country) +\
                '. Este usuario permite registrar y monitorear a los \
                representantes de cada estado que pertenecen a dicho país'
        elif self.request.user.groups.filter(name='Nivel Estadal'):
            state_level = StateLevel.objects.get(profile=profile)
            context['text1'] = 'Bienvenido ' + str(profile)
            context['text2'] = 'Usuario nivel estado ' +\
                str(state_level.state) +\
                '. Este usuario permite registrar y monitorear a los \
                representantes de cada municipio que pertenecen a dicho estado'
        elif self.request.user.groups.filter(name='Nivel Municipal'):
            municipal_level = MunicipalLevel.objects.get(profile=profile)
            context['text1'] = 'Bienvenido ' + str(profile)
            context['text2'] = 'Usuario nivel municipio ' +\
                str(municipal_level.municipality) + ', ' +\
                str(municipal_level.municipality.state) +\
                '. Este usuario permite registrar y monitorear a los \
                representantes de cada parroquia que pertenecen a \
                dicho municipio'
        elif self.request.user.groups.filter(name='Nivel Parroquial'):
            parish_level = ParishLevel.objects.get(profile=profile)
            context['text1'] = 'Bienvenido ' + str(profile)
            context['text2'] = 'Usuario nivel parroquia ' +\
                str(parish_level.parish) + ', ' +\
                str(parish_level.parish.municipality) +\
                ', ' + str(parish_level.parish.municipality.state) +\
                '. Este usuario permite registrar y monitorear a los \
                representantes de cada consejo comunal que pertenecen a \
                dicha parroquia'
        elif self.request.user.groups.filter(name='Nivel Comunal'):
            communal_council_level = CommunalCouncilLevel.objects.get(
                profile=profile
            )
            municipality = communal_council_level.communal_council.parish.\
                municipality
            state = communal_council_level.communal_council.parish.\
                municipality.state
            context['text1'] = 'Bienvenido ' + str(profile)
            context['text2'] = 'Usuario nivel consejo comunal ' +\
                str(communal_council_level.communal_council) + \
                ', ' + str(communal_council_level.communal_council.parish) +\
                ', ' + str(municipality) + ', ' + str(state) +\
                '. Este usuario permite registrar, actualizar, eliminar y \
                listar a todos los adultos mayores'
        return context


class Error403TemplateView(TemplateView):
    """!
    Clase para mostrar error de permiso

    @author William Páez <paez.william8@gmail.com>
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    template_name = 'base/error.403.html'
