from django import forms
from .constant import NACIONALIDAD
from django.utils.translation import ugettext_lazy as _

class CedulaWidget(forms.MultiWidget):
    """!
    Clase que agrupa los widgets de los campos de nacionalidad y número de cédula de identidad

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve) / William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 14-01-2018
    @version 1.0.0
    """

    def __init__(self, *args, **kwargs):

        widgets = (
            forms.Select(
                attrs={
                    'class': 'select2 form-control', 'data-toggle': 'tooltip',
                    'title': _("Seleccione la nacionalidad")
                }, choices=NACIONALIDAD
            ),
            forms.TextInput(
                attrs={
                    'class': 'form-control text-center input-sm', 'placeholder': '00000000', 'data-mask': '00000000',
                    'data-toggle': 'tooltip', 'maxlength': '8', 'size':'7', 'data-rule-required': 'true',
                    'title': _("Indique el número de Cédula de Identidad")
                }
            )
        )

        super(CedulaWidget, self).__init__(widgets, *args, **kwargs)

    def format_output(self, rendered_widgets):
        return ' - '.join(rendered_widgets)

    def decompress(self, value):
        if value:
            return [value[0], value[1:]]
        return [None, None]
