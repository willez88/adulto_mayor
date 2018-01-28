from django import forms
from .constant import NACIONALIDAD
from .widgets import CedulaWidget
from django.utils.translation import ugettext_lazy as _

class CedulaField(forms.MultiValueField):
    """!
    Clase que agrupa los campos de una cédula correspondientes a la nacionalidad y los números

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve) / William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 14-01-2018
    @version 1.0.0
    """

    widget = CedulaWidget
    default_error_messages = {
        'invalid_choices': _("Debe seleccionar una nacionalidad válida")
    }

    def __init__(self, *args, **kwargs):

        error_messages = {
            'required': _("Debe indicar un número de Cédula"),
            'invalid': _("El valor indicado no es válido"),
            'incomplete': _("El número de Cédula esta incompleto")
        }

        fields = (
            forms.ChoiceField(choices=NACIONALIDAD),
            forms.CharField(max_length=8)
        )

        label = _("Cedula de Identidad:")

        super(CedulaField, self).__init__(
            error_messages=error_messages, fields=fields, label=label, require_all_fields=True, *args, **kwargs
        )

    def compress(self, data_list):
        if data_list:
            return ''.join(data_list)
        return ''
