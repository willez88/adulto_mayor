from django.contrib import admin
from .models import CommunalCouncil
from .forms import CommunalCouncilAdminForm

class CommunalCouncilAdmin(admin.ModelAdmin):
    form = CommunalCouncilAdminForm
    change_form_template = 'base/admin/change_form.html'
    list_display = ('rif','name','parish',)
    list_filter = ('parish',)
    ordering = ('parish__name',)

admin.site.register(CommunalCouncil, CommunalCouncilAdmin)
