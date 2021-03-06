from django import forms
from .models import Person
from base.fields import IdentityCardField
from django.utils.translation import ugettext_lazy as _
from django.core import validators
from base.fields import IdentityCardField, PhoneField
from base.models import (
    Gender, MaritalStatus, InstructionDegree, EducationalMission, IncomeType,
    Disease, Disability, SocialMission
)
import re

class PersonForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)

        diseases_list = []
        for di in Disease.objects.all():
            diseases_list.append( (di.id,di) )
        self.fields['diseases'].choices = diseases_list

        disabilities_list = []
        for dis in Disability.objects.all():
            disabilities_list.append( (dis.id,dis) )
        self.fields['disabilities'].choices = disabilities_list

    ## Nombre
    first_name = forms.CharField(
        label=_('Nombres:'),
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-sm', 'data-toggle': 'tooltip',
                'title': _('Indique los Nombres de la Persona'),
            }
        )
    )

    ## Apellido
    last_name = forms.CharField(
        label=_('Apellidos:'),
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-sm', 'data-toggle': 'tooltip',
                'title': _('Indique los Apellidos de la Persona'),
            }
        )
    )

    ## Cédula
    identity_card = IdentityCardField(required=False)

    ## Teléfono del usuario
    phone = PhoneField(
        validators=[
            validators.RegexValidator(
                r'^\+\d{2}-\d{3}-\d{7}$',
                _('Número telefónico inválido. Debe tener el formato que aparece en la ayuda.')
            ),
        ]
    )

    ## Correo del usuario
    email = forms.EmailField(
        label=_('Correo Electrónico:'), max_length=100,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control input-sm email-mask', 'data-toggle': 'tooltip',
                'title': _('Indique el correo electrónico de contacto.')
            }
        ), required = False
    )

    gender = forms.ModelChoiceField(
        label=_('Género:'), queryset=Gender.objects.all(),
        empty_label = _('Seleccione...'),
        widget=forms.Select(
            attrs={
                'class': 'form-control select2', 'data-toggle': 'tooltip',
                'title': _('Seleccione el género'),
            }
        )
    )

    ## Fecha de nacimiento
    birthdate = forms.CharField(
        label=_('Fecha de Nacimieno:'),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm datepicker',
                'readonly':'true',
            }
        )
    )

    marital_status = forms.ModelChoiceField(
        label=_('Estado Civil:'), queryset=MaritalStatus.objects.all(),
        empty_label = _('Seleccione...'),
        widget=forms.Select(
            attrs={
                'class': 'form-control select2', 'data-toggle': 'tooltip',
                'title': _('Seleccione el estado civil'),
            }
        )
    )

    instruction_degree = forms.ModelChoiceField(
        label=_('Grado de Instrucción:'), queryset=InstructionDegree.objects.all(),
        empty_label = _('Seleccione...'),
        widget=forms.Select(
            attrs={
                'class': 'form-control select2', 'data-toggle': 'tooltip',
                'title': _('Seleccione el grado de instrucción'),
            }
        ),
        required = False
    )

    educational_mission = forms.ModelChoiceField(
        label=_('Misión Educativa:'), queryset=EducationalMission.objects.all(),
        empty_label = _('Seleccione...'),
        widget=forms.Select(
            attrs={
                'class': 'form-control select2', 'data-toggle': 'tooltip',
                'title': _('Seleccione la misión educativa'),
            }
        ),
        required = False
    )

    social_mission = forms.ModelChoiceField(
        label=_('Misión Social:'), queryset=SocialMission.objects.all(),
        empty_label = _('Seleccione...'),
        widget=forms.Select(
            attrs={
                'class': 'form-control select2', 'data-toggle': 'tooltip',
                'title': _('Seleccione la misión social'),
            }
        ),
        required = False
    )

    income_type = forms.ModelChoiceField(
        label=_('Tipo de Ingreso:'), queryset=IncomeType.objects.all(),
        empty_label = _('Seleccione...'),
        widget=forms.Select(
            attrs={
                'class': 'form-control select2', 'data-toggle': 'tooltip',
                'title': _('Seleccione el tipo de ingreso'),
            }
        ),
        required = False
    )

    ## ¿Es pensionado?
    pensioner = forms.BooleanField(
        label=_('¿Es Pensionado?'),
        required = False
    )

    ## ¿Es jubilado?
    retired = forms.BooleanField(
        label=_('¿Es Jubilado?'),
        required = False
    )

    ## Enfermedad que presenta la persona
    diseases = forms.MultipleChoiceField(
        label=_('Enfermedad que Presenta:'),
        widget=forms.SelectMultiple(
            attrs={
                'class': 'form-control select2', 'data-toggle': 'tooltip', 'style': 'width:100%',
                'title': _('Indique la enfermedad que presenta la persona'),
            }
        ),
        required = False
    )

    ## Discapacidad que presenta la persona
    disabilities = forms.MultipleChoiceField(
        label=_('Discapacidad que Presenta:'),
        widget=forms.SelectMultiple(
            attrs={
                'class': 'form-control select2', 'data-toggle': 'tooltip',
                'title': _('Indique la Discapacidad que Presenta la Persona'),
                'style': 'width:100%',
            }
        ),
        required = False
    )

    def clean_identity_card(self):
        identity_card = self.cleaned_data['identity_card']
        if identity_card == 'V' or identity_card == 'E':
            identity_card = ''
            return identity_card
        else:
            result = re.match(r'^[VE][\d]{8}$', identity_card)
            if result:
                return identity_card
            else:
                raise forms.ValidationError(_('La cédula es incorrecta'))

    class Meta:

        model = Person
        exclude = [
            'communal_council_level'
        ]
