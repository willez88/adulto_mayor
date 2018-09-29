from django.contrib import admin
from .models import Profile, NationalLevel, StateLevel, MunicipalLevel, ParishLevel, CommunalCouncilLevel
from .forms import CommunalCouncilLevelAdminForm

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','level','phone',)
    list_filter = ('level',)
    ordering = ('user__username',)
    search_fields = ('user__username',)
admin.site.register(Profile, ProfileAdmin)

class NationalLevelAdmin(admin.ModelAdmin):
    list_display = ('profile','country',)
    list_filter = ('country',)
    #list_per_page = 25
    #ordering = ('country',)
    search_fields = ('profile__user__username',)
admin.site.register(NationalLevel, NationalLevelAdmin)

class StateLevelAdmin(admin.ModelAdmin):
    list_display = ('profile','state',)
    list_filter = ('state',)
    search_fields = ('profile__user__username',)
admin.site.register(StateLevel, StateLevelAdmin)

class MunicipalLevelAdmin(admin.ModelAdmin):
    list_display = ('profile','municipality',)
    list_filter = ('municipality',)
    search_fields = ('profile__user__username',)
admin.site.register(MunicipalLevel, MunicipalLevelAdmin)

class ParishLevelAdmin(admin.ModelAdmin):
    list_display = ('profile','parish',)
    list_filter = ('parish',)
    search_fields = ('profile__user__username',)
admin.site.register(ParishLevel, ParishLevelAdmin)

class CommunalCouncilLevelAdmin(admin.ModelAdmin):
    form = CommunalCouncilLevelAdminForm
    change_form_template = 'user/admin/change_form.html'

    list_display = ('profile','communal_council',)
    list_filter = ('communal_council',)
    search_fields = ('profile__user__username',)
admin.site.register(CommunalCouncilLevel, CommunalCouncilLevelAdmin)
