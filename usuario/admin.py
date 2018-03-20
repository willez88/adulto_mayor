from django.contrib import admin
from .models import Perfil, Nacional, Estadal, Municipal, Parroquial, Comunal

# Register your models here.

class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user','nivel','telefono',)
    list_filter = ('user','nivel','telefono',)
    list_per_page = 25
    ordering = ('user',)
    search_fields = ('telefono','nivel','user',)
admin.site.register(Perfil, PerfilAdmin)

class NacionalAdmin(admin.ModelAdmin):
    list_display = ('perfil','pais',)
    list_filter = ('perfil','pais',)
    list_per_page = 25
    ordering = ('pais',)
    search_fields = ('pais','perfil',)
admin.site.register(Nacional, NacionalAdmin)

class EstadalAdmin(admin.ModelAdmin):
    list_display = ('perfil','estado',)
    list_filter = ('perfil','estado',)
    list_per_page = 25
    ordering = ('estado',)
    search_fields = ('estado','perfil',)
admin.site.register(Estadal, EstadalAdmin)

class MunicipalAdmin(admin.ModelAdmin):
    list_display = ('perfil','municipio',)
    list_filter = ('perfil','municipio',)
    list_per_page = 25
    ordering = ('perfil',)
    search_fields = ('municipio','perfil',)
admin.site.register(Municipal, MunicipalAdmin)

class ParroquialAdmin(admin.ModelAdmin):
    list_display = ('perfil','parroquia',)
    list_filter = ('perfil','parroquia',)
    list_per_page = 25
    ordering = ('parroquia',)
    search_fields = ('municipio','perfil',)
admin.site.register(Parroquial, ParroquialAdmin)

class ComunalAdmin(admin.ModelAdmin):
    list_display = ('perfil','consejo_comunal',)
    list_filter = ('perfil','consejo_comunal',)
    list_per_page = 25
    ordering = ('consejo_comunal',)
    search_fields = ('parroquia','perfil',)
admin.site.register(Comunal, ComunalAdmin)
