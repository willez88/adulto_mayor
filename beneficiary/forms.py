import re

from base.fields import IdentityCardField, PhoneField
from base.models import (
    Disability, Disease, EducationalMission, Gender, IncomeType,
    InstructionDegree, MaritalStatus, SocialMission,
)
from django import forms
from django.core import validators

from .models import Person


class PersonForm(forms.ModelForm):
    """!
    Clase que contiene los campos del formulario

    @author William Páez <paez.william8@gmail.com>
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    def __init__(self, *args, **kwargs):
        """!
        Método que permite inicializar el formulario

        @author William Páez <paez.william8@gmail.com>
        @param self <b>{object}</b> Objeto que instancia la clase
        @param *args <b>{tupla}</b> Tupla de valores, inicialmente vacia
        @param *kwargs <b>{dict}</b> Diccionario de datos, inicialmente vacio
        """

        super().__init__(*args, **kwargs)
        diseases_list = []
        for di in Disease.objects.all():
            diseases_list.append((di.id, di))
        self.fields['diseases'].choices = diseases_list

        disabilities_list = []
        for dis in Disability.objects.all():
            disabilities_list.append((dis.id, dis))
        self.fields['disabilities'].choices = disabilities_list

    # Nombre
    first_name = forms.CharField(
        label='Nombres:',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-sm',
                'data-toggle': 'tooltip',
                'title': 'Indique los Nombres de la Persona',
            }
        )
    )

    # Apellido
    last_name = forms.CharField(
        label='Apellidos:',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-sm',
                'data-toggle': 'tooltip',
                'title': 'Indique los Apellidos de la Persona',
            }
        )
    )

    # Cédula
    identity_card = IdentityCardField(required=False)

    # Teléfono del usuario
    phone = PhoneField(
        validators=[
            validators.RegexValidator(
                r'^\+\d{2}-\d{3}-\d{7}$',
                'Número telefónico inválido. Debe tener el formato que \
                    aparece en la ayuda.'
            ),
        ]
    )

    # Correo del usuario
    email = forms.EmailField(
        label='Correo Electrónico:', max_length=100,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control input-sm email-mask',
                'data-toggle': 'tooltip',
                'title': 'Indique el correo electrónico de contacto.'
            }
        ), required=False
    )

    # Género
    gender = forms.ModelChoiceField(
        label='Género:',
        queryset=Gender.objects.all(),
        empty_label='Seleccione...',
        widget=forms.Select(
            attrs={
                'class': 'form-control select2', 'data-toggle': 'tooltip',
                'title': 'Seleccione el género',
            }
        )
    )

    # Fecha de nacimiento
    birthdate = forms.CharField(
        label='Fecha de Nacimieno:',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm datepicker',
                'readonly': 'true',
            }
        )
    )

    # Estado civil
    marital_status = forms.ModelChoiceField(
        label='Estado Civil:',
        queryset=MaritalStatus.objects.all(),
        empty_label='Seleccione...',
        widget=forms.Select(
            attrs={
                'class': 'form-control select2', 'data-toggle': 'tooltip',
                'title': 'Seleccione el estado civil',
            }
        )
    )

    # Grado de instrucción
    instruction_degree = forms.ModelChoiceField(
        label='Grado de Instrucción:',
        queryset=InstructionDegree.objects.all(),
        empty_label='Seleccione...',
        widget=forms.Select(
            attrs={
                'class': 'form-control select2', 'data-toggle': 'tooltip',
                'title': 'Seleccione el grado de instrucción',
            }
        ),
        required=False
    )

    # Misión educativa
    educational_mission = forms.ModelChoiceField(
        label='Misión Educativa:',
        queryset=EducationalMission.objects.all(),
        empty_label='Seleccione...',
        widget=forms.Select(
            attrs={
                'class': 'form-control select2', 'data-toggle': 'tooltip',
                'title': 'Seleccione la misión educativa',
            }
        ),
        required=False
    )

    # Misión social
    social_mission = forms.ModelChoiceField(
        label='Misión Social:',
        queryset=SocialMission.objects.all(),
        empty_label='Seleccione...',
        widget=forms.Select(
            attrs={
                'class': 'form-control select2', 'data-toggle': 'tooltip',
                'title': 'Seleccione la misión social',
            }
        ),
        required=False
    )

    # Tipo de ingreso
    income_type = forms.ModelChoiceField(
        label='Tipo de Ingreso:',
        queryset=IncomeType.objects.all(),
        empty_label='Seleccione...',
        widget=forms.Select(
            attrs={
                'class': 'form-control select2', 'data-toggle': 'tooltip',
                'title': 'Seleccione el tipo de ingreso',
            }
        ),
        required=False
    )

    # ¿Es pensionado?
    pensioner = forms.BooleanField(
        label='¿Es Pensionado?',
        required=False
    )

    # ¿Es jubilado?
    retired = forms.BooleanField(
        label='¿Es Jubilado?',
        required=False
    )

    # Enfermedades que presenta la persona
    diseases = forms.MultipleChoiceField(
        label='Enfermedades que Presenta:',
        widget=forms.SelectMultiple(
            attrs={
                'class': 'form-control select2', 'data-toggle': 'tooltip',
                'style': 'width:100%',
                'title': 'Indique la enfermedad que presenta la persona',
            }
        ),
        required=False
    )

    # Discapacidad que presenta la persona
    disabilities = forms.MultipleChoiceField(
        label='Discapacidades que Presenta:',
        widget=forms.SelectMultiple(
            attrs={
                'class': 'form-control select2', 'data-toggle': 'tooltip',
                'title': 'Indique la Discapacidad que Presenta la Persona',
                'style': 'width:100%',
            }
        ),
        required=False
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
                raise forms.ValidationError('La cédula es incorrecta')

    class Meta:
        """!
        Meta clase del modelo que establece algunas propiedades

        @author William Páez <paez.william8@gmail.com>
        """

        model = Person
        exclude = [
            'communal_council_level'
        ]
