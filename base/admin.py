from django.contrib import admin

from .forms import CommunalCouncilAdminForm
from .models import (
    CommunalCouncil, Disability, Disease, EducationalMission, Gender,
    IncomeType, InstructionDegree, MaritalStatus, SocialMission,
)


class CommunalCouncilAdmin(admin.ModelAdmin):
    """!
    Clase que agrega modelo CommunalCouncil al panel administrativo

    @author William Páez <paez.william8@gmail.com>
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    form = CommunalCouncilAdminForm
    change_form_template = 'base/admin/change_form.html'
    list_display = ('rif', 'name', 'parish',)
    list_filter = ('parish__municipality__state', 'parish__municipality',)
    search_fields = ('rif', 'name', 'parish__name',)


class MaritalStatusAdmin(admin.ModelAdmin):
    """!
    Clase que agrega modelo MaritalStatus al panel administrativo

    @author William Páez <paez.william8@gmail.com>
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    list_display = ('name',)
    search_fields = ('name',)


class InstructionDegreeAdmin(admin.ModelAdmin):
    """!
    Clase que agrega modelo InstructionDegree al panel administrativo

    @author William Páez <paez.william8@gmail.com>
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    list_display = ('name',)
    search_fields = ('name',)


class EducationalMissionAdmin(admin.ModelAdmin):
    """!
    Clase que agrega modelo EducationalMission al panel administrativo

    @author William Páez <paez.william8@gmail.com>
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    list_display = ('name',)
    search_fields = ('name',)


class SocialMissionAdmin(admin.ModelAdmin):
    """!
    Clase que agrega modelo SocialMission al panel administrativo

    @author William Páez <paez.william8@gmail.com>
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    list_display = ('name',)
    search_fields = ('name',)


class IncomeTypeAdmin(admin.ModelAdmin):
    """!
    Clase que agrega modelo IncomeType al panel administrativo

    @author William Páez <paez.william8@gmail.com>
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    list_display = ('name',)
    search_fields = ('name',)


class GenderAdmin(admin.ModelAdmin):
    """!
    Clase que agrega modelo Gender al panel administrativo

    @author William Páez <paez.william8@gmail.com>
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    list_display = ('name',)
    search_fields = ('name',)


class DiseaseAdmin(admin.ModelAdmin):
    """!
    Clase que agrega modelo DiseaseAdmin al panel administrativo

    @author William Páez <paez.william8@gmail.com>
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    list_display = ('name',)
    search_fields = ('name',)


class DisabilityAdmin(admin.ModelAdmin):
    """!
    Clase que agrega modelo Disability al panel administrativo

    @author William Páez <paez.william8@gmail.com>
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(CommunalCouncil, CommunalCouncilAdmin)
admin.site.register(MaritalStatus, MaritalStatusAdmin)
admin.site.register(InstructionDegree, InstructionDegreeAdmin)
admin.site.register(EducationalMission, EducationalMissionAdmin)
admin.site.register(SocialMission, SocialMissionAdmin)
admin.site.register(IncomeType, IncomeTypeAdmin)
admin.site.register(Gender, GenderAdmin)
admin.site.register(Disease, DiseaseAdmin)
admin.site.register(Disability, DisabilityAdmin)
