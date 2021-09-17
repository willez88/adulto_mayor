from django.contrib import admin

from .models import Person


class PersonAdmin(admin.ModelAdmin):
    """!
    Clase que agrega modelo CommunalCouncil al panel administrativo

    @author William Páez <wpaez@cenditel.gob.ve> | <paez.william8@gmail.com>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    list_display = ('first_name', 'last_name', 'identity_card',)
    search_fields = ('identity_card',)


admin.site.register(Person, PersonAdmin)
