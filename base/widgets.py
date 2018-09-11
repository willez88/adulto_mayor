from django import forms
from .constant import NATIONALITY, RIF_TYPE, PHONE_PREFIX
from django.utils.translation import ugettext_lazy as _

class RifWidget(forms.MultiWidget):

    def __init__(self, attrs=None, *args, **kwargs):

        self.attrs = attrs or {}

        widgets = (
            forms.Select(
                attrs={
                    'class': 'select2 form-control', 'data-toggle': 'tooltip',
                    'title': _('Seleccione el tipo de R.I.F.')
                }, choices=RIF_TYPE
            ),
            forms.TextInput(
                attrs={
                    'class': 'form-control text-center', 'placeholder': '00000000', 'data-mask': '00000000',
                    'data-toggle': 'tooltip', 'maxlength': '8','size':'7',
                    'title': _('Indique el número de R.I.F., si es menor a 8 dígitos complete con ceros a la izquierda.')
                }
            ),
            forms.TextInput(
                attrs={
                    'class': 'form-control text-center', 'data-mask': '0',
                    'title': _('Indique el último dígito del R.I.F.'), 'placeholder': '0', 'maxlength': '1',
                    'size': '1', 'data-toggle': 'tooltip',
                }
            )
        )

        super(RifWidget, self).__init__(widgets, attrs, *args, **kwargs)

    def format_output(self, rendered_widgets):
        return ' - '.join(rendered_widgets)

    def decompress(self, value):
        if value:
            return [value[0], value[1:-1], value[-1]]
        return [None, None, None]

class IdentityCardWidget(forms.MultiWidget):

    def __init__(self, *args, **kwargs):

        widgets = (
            forms.Select(
                attrs={
                    'class': 'select2 form-control', 'data-toggle': 'tooltip',
                    'title': _('Seleccione la nacionalidad.')
                }, choices=NATIONALITY
            ),
            forms.TextInput(
                attrs={
                    'class': 'form-control text-center input-sm', 'placeholder': '00000000', 'data-mask': '00000000',
                    'data-toggle': 'tooltip',
                    'title': _('Indique el número de Cédula de Identidad.')
                }
            )
        )

        super(IdentityCardWidget, self).__init__(widgets, *args, **kwargs)

    def format_output(self, rendered_widgets):
        return ' - '.join(rendered_widgets)

    def decompress(self, value):
        if value:
            return [value[0], value[1:]]
        return [None, None]

class PhoneWidget(forms.MultiWidget):

    def __init__(self, *args, **kwargs):

        widgets = (
            forms.Select(
                attrs={
                    'class': 'select2 form-control', 'data-toggle': 'tooltip',
                    'title': _('Seleccione el código telefónico de país.')
                }, choices=PHONE_PREFIX
            ),
            forms.TextInput(
                attrs={
                    'class': 'form-control input-sm', 'placeholder': '-000-0000000', 'data-mask': '-000-0000000',
                    'data-toggle': 'tooltip',
                    'title': _('Indique el número de teléfono.')
                }
            )
        )

        super(PhoneWidget, self).__init__(widgets, *args, **kwargs)

    def format_output(self, rendered_widgets):
        return ' - '.join(rendered_widgets)

    def decompress(self, value):
        if value:
            return [value[0:4], value[4:]]
        return [None, None]
