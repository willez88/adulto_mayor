from django.contrib import admin

from .forms import CommunalCouncilLevelAdminForm
from .models import (
    CommunalCouncilLevel, MunicipalLevel, NationalLevel, ParishLevel,
    Profile, StateLevel,
)


class ProfileAdmin(admin.ModelAdmin):
    """!
    Clase que agrega modelo Profile al panel administrativo

    @author William Páez <wpaez@cenditel.gob.ve> | <paez.william8@gmail.com>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    list_display = ('user', 'phone',)
    ordering = ('user__username',)
    search_fields = ('user__username',)


class NationalLevelAdmin(admin.ModelAdmin):
    """!
    Clase que agrega modelo NationalLevel al panel administrativo

    @author William Páez <wpaez@cenditel.gob.ve> | <paez.william8@gmail.com>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    list_display = ('profile', 'country',)
    list_filter = ('country',)
    # list_per_page = 25
    # ordering = ('country',)
    search_fields = ('profile__user__username',)


class StateLevelAdmin(admin.ModelAdmin):
    """!
    Clase que agrega modelo StateLevel al panel administrativo

    @author William Páez <wpaez@cenditel.gob.ve> | <paez.william8@gmail.com>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    list_display = ('profile', 'state',)
    list_filter = ('state',)
    search_fields = ('profile__user__username',)


class MunicipalLevelAdmin(admin.ModelAdmin):
    """!
    Clase que agrega modelo MunicipalLevel al panel administrativo

    @author William Páez <wpaez@cenditel.gob.ve> | <paez.william8@gmail.com>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    list_display = ('profile', 'municipality',)
    list_filter = ('municipality',)
    search_fields = ('profile__user__username',)


class ParishLevelAdmin(admin.ModelAdmin):
    """!
    Clase que agrega modelo ParishLevel al panel administrativo

    @author William Páez <wpaez@cenditel.gob.ve> | <paez.william8@gmail.com>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    list_display = ('profile', 'parish',)
    list_filter = ('parish',)
    search_fields = ('profile__user__username',)


class CommunalCouncilLevelAdmin(admin.ModelAdmin):
    """!
    Clase que agrega modelo CommunalCouncilLevel al panel administrativo

    @author William Páez <wpaez@cenditel.gob.ve> | <paez.william8@gmail.com>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    form = CommunalCouncilLevelAdminForm
    change_form_template = 'user/admin/change_form.html'

    list_display = ('profile', 'communal_council',)
    list_filter = ('communal_council',)
    search_fields = ('profile__user__username',)


admin.site.register(Profile, ProfileAdmin)
admin.site.register(NationalLevel, NationalLevelAdmin)
admin.site.register(StateLevel, StateLevelAdmin)
admin.site.register(MunicipalLevel, MunicipalLevelAdmin)
admin.site.register(ParishLevel, ParishLevelAdmin)
admin.site.register(CommunalCouncilLevel, CommunalCouncilLevelAdmin)
