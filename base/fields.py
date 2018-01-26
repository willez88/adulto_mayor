from django.forms import MultiValueField, ChoiceField, CharField, TextInput
from .constant import NACIONALIDAD
from .widgets import CedulaWidget
from django.utils.translation import ugettext_lazy as _

class CedulaField(MultiValueField):

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
            ChoiceField(choices=NACIONALIDAD),
            CharField(max_length=8)
        )

        label = _("Cedula de Identidad:")

        super(CedulaField, self).__init__(
            error_messages=error_messages, fields=fields, label=label, require_all_fields=True, *args, **kwargs
        )

    def compress(self, data_list):
        if data_list:
            return ''.join(data_list)
        return ''
