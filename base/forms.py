from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import State, Municipality, Parish, CommunalCouncil
from .fields import RifField

class CommunalCouncilAdminForm(forms.ModelForm):

    ## Rif del consejo comunal
    rif = RifField()

    ## Nombre del consejo comunal
    name = forms.CharField(
        label=_("Nombre del Consejo Comunal:"),
        max_length=500,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip',
                'title': _("Indique el Nombre del RIF"),
            }
        )
    )

    ## Estado donde se ecnuetra ubicado el municipio
    state = forms.ModelChoiceField(
        label=_("Estado:"), queryset=State.objects.all(), empty_label=_("Seleccione..."),
        widget=forms.Select(attrs={
            'class': 'form-control select2', 'data-toggle': 'tooltip',
            'title': _("Seleccione el estado en donde se encuentra ubicada"),
        })
    )

    ## Municipio donde se encuentra ubicada la parroquia
    municipality = forms.ModelChoiceField(
        label=_("Municipio:"), queryset=Municipality.objects.all(), empty_label=_("Seleccione..."),
        widget=forms.Select(attrs={
            'class': 'form-control select2', 'data-toggle': 'tooltip', 'disabled': 'true',
            'title': _("Seleccione el municipio en donde se encuentra ubicada"),
        })
    )

    ## Parroquia donde se encuentra ubicado el consejo comunal
    parish = forms.ModelChoiceField(
        label=_("Parroquia:"), queryset=Parish.objects.all(), empty_label=_("Seleccione..."),
        widget=forms.Select(attrs={
            'class': 'form-control select2', 'data-toggle': 'tooltip', 'disabled': 'true',
            'title': _("Seleccione la parroquia en donde se encuentra ubicada"),
        })
    )

    class Meta:

        model = CommunalCouncil
        fields = [
            'rif','name','state','municipality','parish'
        ]
