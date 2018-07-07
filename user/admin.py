from django.contrib import admin
from .models import Profile, NationalLevel, StateLevel, MunicipalLevel, ParishLevel, CommunalCouncilLevel

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','level','phone',)
    list_filter = ('level',)
    list_per_page = 25
    ordering = ('user',)
    #search_fields = ('telefono','nivel','user',)
admin.site.register(Profile, ProfileAdmin)

class NationalLevelAdmin(admin.ModelAdmin):
    list_display = ('profile','country',)
    list_filter = ('profile','country',)
    list_per_page = 25
    ordering = ('country',)
    #search_fields = ('pais','perfil',)
admin.site.register(NationalLevel, NationalLevelAdmin)

class StateLevelAdmin(admin.ModelAdmin):
    list_display = ('profile','state',)
    list_filter = ('profile','state',)
    list_per_page = 25
    ordering = ('state',)
    #search_fields = ('estado','perfil',)
admin.site.register(StateLevel, StateLevelAdmin)

class MunicipalLevelAdmin(admin.ModelAdmin):
    list_display = ('profile','municipality',)
    list_filter = ('profile','municipality',)
    list_per_page = 25
    ordering = ('municipality',)
    #search_fields = ('municipio','perfil',)
admin.site.register(MunicipalLevel, MunicipalLevelAdmin)

class ParishLevelAdmin(admin.ModelAdmin):
    list_display = ('profile','parish',)
    list_filter = ('profile','parish',)
    list_per_page = 25
    ordering = ('parish',)
    #search_fields = ('municipio','perfil',)
admin.site.register(ParishLevel, ParishLevelAdmin)

class CommunalCouncilLevelAdmin(admin.ModelAdmin):
    list_display = ('profile','communal_council',)
    list_filter = ('profile','communal_council',)
    list_per_page = 25
    ordering = ('communal_council',)
    #search_fields = ('parroquia','perfil',)
admin.site.register(CommunalCouncilLevel, CommunalCouncilLevelAdmin)
