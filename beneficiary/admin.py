from django.contrib import admin

from .models import Person


class PersonAdmin(admin.ModelAdmin):
    """!
    Clase que agrega modelo CommunalCouncil al panel administrativo

    @author William Páez <paez.william8@gmail.com>
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    list_display = ('first_name', 'last_name', 'identity_card',)
    search_fields = ('identity_card',)


admin.site.register(Person, PersonAdmin)
