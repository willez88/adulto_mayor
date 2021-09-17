from django import template
from django.contrib.auth.models import Group

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    """!
    Método para verificar si el usuario pertenece al grupo

    @author William Páez <wpaez@cenditel.gob.ve> | <paez.william8@gmail.com>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False
