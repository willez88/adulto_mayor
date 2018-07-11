from django.contrib import admin
from .models import CommunalCouncil
from .forms import CommunalCouncilAdminForm

class CommunalCouncilAdmin(admin.ModelAdmin):
    form = CommunalCouncilAdminForm
    change_form_template = 'base/admin/change_form.html'
    list_display = ('rif','name','parish',)
    list_filter = ('parish',)
    #list_per_page = 25
    ordering = ('parish',)

admin.site.register(CommunalCouncil, CommunalCouncilAdmin)
