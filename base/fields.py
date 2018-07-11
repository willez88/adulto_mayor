from django import forms
from .constant import NATIONALITY, RIF_TYPE, PHONE_PREFIX
from .widgets import RifWidget, IdentificationCardWidget, PhoneWidget
from django.utils.translation import ugettext_lazy as _

class RifField(forms.MultiValueField):
    widget = RifWidget
    default_error_messages = {
        'invalid_choices': _("Debe seleccionar un tipo de RIF válido")
    }

    def __init__(self, *args, **kwargs):

        error_messages = {
            'required': _("Debe indicar un numero de RIF"),
            'invalid': _("El valor indicado no es válido"),
            'incomplete': _("El número de RIF esta incompleto")
        }

        fields = (
            forms.ChoiceField(choices=RIF_TYPE),
            forms.CharField(max_length=8, min_length=8),
            forms.CharField(max_length=1, min_length=1)
        )

        label = _("R.I.F.:")

        help_text = _('C-00000000-0')

        super(RifField, self).__init__(
            error_messages=error_messages, fields=fields, label=label, help_text=help_text, require_all_fields=True, *args, **kwargs
        )

    def compress(self, data_list):

        if data_list:
            return ''.join(data_list)
        return ''

class IdentificationCardField(forms.MultiValueField):
    widget = IdentificationCardWidget
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
            forms.ChoiceField(choices=NATIONALITY),
            forms.CharField(max_length=8)
        )

        label = _("Cédula de Identidad:")

        help_text = _("V-00000000 ó E-00000000")

        super(IdentificationCardField, self).__init__(
            error_messages=error_messages, fields=fields, label=label, help_text=help_text, require_all_fields=True, *args, **kwargs
        )

    def compress(self, data_list):
        if data_list:
            return ''.join(data_list)
        return ''

class PhoneField(forms.MultiValueField):
    widget = PhoneWidget
    default_error_messages = {
        'invalid_choices': _("Debe seleccionar un prefijo de teléfono de país válido")
    }

    def __init__(self, *args, **kwargs):

        error_messages = {
            'required': _("Debe indicar un número de Teléfono"),
            'invalid': _("El valor indicado no es válido"),
            'incomplete': _("El número de teléfono esta incompleto")
        }

        fields = (
            forms.ChoiceField(choices=PHONE_PREFIX),
            forms.CharField(max_length=12)
        )

        label = _("Teléfono:")

        help_text = _("+58-416-0000000")

        super(PhoneField, self).__init__(
            error_messages=error_messages, fields=fields, label=label, require_all_fields=True, help_text=help_text, *args, **kwargs
        )

    def compress(self, data_list):
        if data_list:
            return ''.join(data_list)
        return ''
