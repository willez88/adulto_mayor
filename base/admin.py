from django.contrib import admin
from .models import (
    CommunalCouncil, MaritalStatus, InstructionDegree, EducationalMission,
    SocialMission, IncomeType, Gender, Disease, Disability
)
from .forms import CommunalCouncilAdminForm

class CommunalCouncilAdmin(admin.ModelAdmin):
    form = CommunalCouncilAdminForm
    change_form_template = 'base/admin/change_form.html'
    list_display = ('rif','name','parish',)
    list_filter = ('parish__municipality__state','parish__municipality',)
    search_fields = ('rif','name','parish__name',)

class MaritalStatusAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class InstructionDegreeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class EducationalMissionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class SocialMissionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class IncomeTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class GenderAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class DiseaseAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class DisabilityAdmin(admin.ModelAdmin):
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
