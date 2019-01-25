from django.contrib import admin
from .models import Person

# Register your models here.

class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','identity_card',)
    search_fields = ('identity_card',)

admin.site.register(Person, PersonAdmin)
