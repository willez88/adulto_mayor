from django.contrib import admin
from .models import Perfil, Estadal, Municipal, Parroquial

# Register your models here.

class PerfilAdmin(admin.ModelAdmin):
    list_display = ('telefono','nivel','user',)
    list_filter = ('telefono','nivel','user',)
    list_per_page = 25
    ordering = ('user',)
    search_fields = ('telefono','nivel','user',)

## Registra el modelo ConsejoComunal en el panel administrativo
admin.site.register(Perfil, PerfilAdmin)

class EstadalAdmin(admin.ModelAdmin):
    list_display = ('estado','perfil',)
    list_filter = ('estado','perfil',)
    list_per_page = 25
    ordering = ('estado',)
    search_fields = ('estado','perfil',)

## Registra el modelo ConsejoComunal en el panel administrativo
admin.site.register(Estadal, EstadalAdmin)

class MunicipalAdmin(admin.ModelAdmin):
    list_display = ('municipio','perfil',)
    list_filter = ('municipio','perfil',)
    list_per_page = 25
    ordering = ('municipio',)
    search_fields = ('municipio','perfil',)

## Registra el modelo ConsejoComunal en el panel administrativo
admin.site.register(Municipal, MunicipalAdmin)
