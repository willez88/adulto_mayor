from django.contrib import admin
from .models import Profile, NationalLevel, StateLevel, MunicipalLevel, ParishLevel, CommunalCouncilLevel
from .forms import CommunalCouncilLevelAdminForm

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','level','phone',)
    list_filter = ('level',)
    #list_per_page = 25
    ordering = ('user__username',)
    #search_fields = ('telefono','nivel','user',)
admin.site.register(Profile, ProfileAdmin)

class NationalLevelAdmin(admin.ModelAdmin):
    list_display = ('profile','country',)
    list_filter = ('country',)
    #list_per_page = 25
    ordering = ('country',)
    #search_fields = ('pais','perfil',)
admin.site.register(NationalLevel, NationalLevelAdmin)

class StateLevelAdmin(admin.ModelAdmin):
    list_display = ('profile','state',)
    list_filter = ('state',)
    #list_per_page = 25
    ordering = ('state',)
    #search_fields = ('estado','perfil',)
admin.site.register(StateLevel, StateLevelAdmin)

class MunicipalLevelAdmin(admin.ModelAdmin):
    list_display = ('profile','municipality',)
    list_filter = ('municipality',)
    #list_per_page = 25
    ordering = ('municipality',)
    #search_fields = ('municipio','perfil',)
admin.site.register(MunicipalLevel, MunicipalLevelAdmin)

class ParishLevelAdmin(admin.ModelAdmin):
    list_display = ('profile','parish',)
    list_filter = ('parish',)
    #list_per_page = 25
    ordering = ('parish',)
    #search_fields = ('municipio','perfil',)
admin.site.register(ParishLevel, ParishLevelAdmin)

class CommunalCouncilLevelAdmin(admin.ModelAdmin):
    form = CommunalCouncilLevelAdminForm
    change_form_template = 'user/admin/change_form.html'

    list_display = ('profile','communal_council',)
    list_filter = ('communal_council',)
    #list_per_page = 25
    ordering = ('communal_council',)
    #search_fields = ('parroquia','perfil',)
admin.site.register(CommunalCouncilLevel, CommunalCouncilLevelAdmin)
