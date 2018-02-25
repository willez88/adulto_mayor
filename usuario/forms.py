from django import forms
from django.contrib.auth.models import User
from base.models import Estado, Municipio, Parroquia, ConsejoComunal
from django.utils.translation import ugettext_lazy as _
from django.core import validators
from base.fields import CedulaField
from .models import Estadal, Municipal, Parroquial, Comunal

class PerfilForm(forms.ModelForm):
    """!
    Clase que contiene los campos del formulario de perfil del usuario

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 14-01-2018
    @version 1.0.0
    """

    ## Username para identificar al usuario, en este caso se usa la cédula
    username = CedulaField(
        validators=[
            validators.RegexValidator(
                r'^[VE][\d]{8}$',
                _("Introduzca un número de cédula válido. Solo se permiten números y una longitud de 8 carácteres. Se agregan ceros (0) si la longitud es de 7 o menos caracteres.")
            ),
        ], help_text=_("V00000000 ó E00000000")
    )

    ## Nombres del usuario
    first_name = forms.CharField(
        label=_("Nombres:"), max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip', 'style':'width:250px;',
                'title': _("Indique los Nombres"),
            }
        )
    )

    ## Apellidos del usuario
    last_name = forms.CharField(
        label=_("Apellidos:"), max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip', 'style':'width:250px;',
                'title': _("Indique los Apellidos"),
            }
        )
    )

    ## Correo del usuario
    email = forms.EmailField(
        label=_("Correo Electrónico:"), max_length=100,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control input-sm email-mask', 'data-toggle': 'tooltip', 'data-rule-required': 'true', 'style':'width:250px;',
                'title': _("Indique el correo electrónico de contacto")
            }
        )
    )

    ## Teléfono del usuario
    telefono = forms.CharField(
        label=_("Teléfono:"),
        max_length=15,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm', 'data-rule-required': 'true', 'data-toggle': 'tooltip', 'style':'width:250px;',
                'title': _("Indique el número telefónico de contacto"), 'data-mask': '+00-000-0000000'
            }
        ),
        validators=[
            validators.RegexValidator(
                r'^\+\d{2}-\d{3}-\d{7}$',
                _("Número telefónico inválido. Solo se permiten números y los símbolos: + -")
            ),
        ],
        help_text=_("+58-416-0000000")
    )

    ## Clave de acceso del usuario
    password = forms.CharField(
        label=_("Contraseña:"), max_length=128,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control input-sm', 'data-rule-required': 'true', 'data-toggle': 'tooltip', 'style':'width:250px;',
                'title': _("Indique una contraseña de aceso al sistema")
            }
        )
    )

    ## Confirmación de clave de acceso del usuario
    verificar_contrasenha = forms.CharField(
        label=_("Verificar Contraseña:"), max_length=128,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control input-sm', 'data-rule-required': 'true', 'data-toggle': 'tooltip', 'style':'width:250px;',
                'title': _("Indique nuevamente la contraseña de aceso al sistema")
            }
        )
    )

    def clean_verificar_contrasenha(self):
        verificar_contrasenha = self.cleaned_data['verificar_contrasenha']
        contrasenha = self.data['password']
        if contrasenha != verificar_contrasenha:
            raise forms.ValidationError(_("La contraseña no es la misma"))

        return verificar_contrasenha

    class Meta:
        """!
        Meta clase del formulario que establece algunas propiedades

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        model = User
        exclude = ['perfil','nivel','date_joined']

class EstadalUpdateForm(PerfilForm):
    """!
    Clase que contiene el formulario para poder actualizar los datos de un usuario que tiene nivel estadal

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 14-01-2018
    @version 1.0.0
    """

    def __init__(self, *args, **kwargs):
        """!
        Función que inicializa el formulario

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        super(EstadalUpdateForm, self).__init__(*args, **kwargs)
        self.fields['password'].required = False
        self.fields['verificar_contrasenha'].required = False
        self.fields['password'].widget.attrs['disabled'] = True
        self.fields['verificar_contrasenha'].widget.attrs['disabled'] = True

    ## Estado donde se encuentra el usuario
    estado = forms.ModelChoiceField(
        label=_("Estado"), queryset=Estado.objects.all(), empty_label=_("Seleccione..."),
        widget=forms.Select(attrs={
            'class': 'form-control select2', 'data-toggle': 'tooltip', 'style':'width:250px;',
            'title': _("Seleccione el estado"),
        })
    )

    def clean_verificar_contrasenha(self):
        pass

    class Meta:
        """!
        Meta clase del formulario que establece algunas propiedades

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        model = User
        exclude = [
            'perfil','nivel','password','verificar_contrasenha','date_joined','last_login','is_active',
            'is_superuser','is_staff'
        ]

class MunicipalForm(PerfilForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(MunicipalForm, self).__init__(*args, **kwargs)
        estadal = Estadal.objects.get(perfil=user.perfil)
        lista_municipio = [('','Selecione...')]
        for mu in Municipio.objects.filter(estado=estadal.estado):
            lista_municipio.append( (mu.id,mu.nombre) )
        self.fields['municipio'].choices = lista_municipio

    municipio = forms.ChoiceField(
        label=_("Municipio"),
        widget=forms.Select(attrs={
            'class': 'form-control select2', 'data-toggle': 'tooltip', 'style':'width:250px;',
            'title': _("Seleccione el municipio"),
        })
    )

    def clean_municipio(self):
        municipio = self.cleaned_data['municipio']

        if Municipal.objects.filter(municipio=municipio):
            raise forms.ValidationError(_("Ya existe un usuario asignado a este municipio"))

        return municipio

class MunicipalUpdateForm(PerfilForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(MunicipalUpdateForm, self).__init__(*args, **kwargs)
        self.fields['password'].required = False
        self.fields['verificar_contrasenha'].required = False
        self.fields['password'].widget.attrs['disabled'] = True
        self.fields['verificar_contrasenha'].widget.attrs['disabled'] = True
        municipal = Municipal.objects.get(perfil=user.perfil)
        lista_municipio = [('','Selecione...')]
        for mu in Municipio.objects.filter(estado=municipal.municipio.estado):
            lista_municipio.append( (mu.id,mu.nombre) )
        self.fields['municipio'].choices = lista_municipio

    municipio = forms.ChoiceField(
        label=_("Municipio"),
        widget=forms.Select(attrs={
            'class': 'form-control select2', 'data-toggle': 'tooltip', 'style':'width:250px;',
            'title': _("Seleccione el municipio"),
        })
    )

    def clean_verificar_contrasenha(self):
        pass

    class Meta:
        model = User
        exclude = [
            'perfil','nivel','password','verificar_contrasenha','date_joined','last_login','is_active',
            'is_superuser','is_staff'
        ]

class ParroquialForm(PerfilForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ParroquialForm, self).__init__(*args, **kwargs)
        municipal = Municipal.objects.get(perfil=user.perfil)
        lista_parroquia = [('','Selecione...')]
        for pa in Parroquia.objects.filter(municipio=municipal.municipio):
            lista_parroquia.append( (pa.id,pa.nombre) )
        self.fields['parroquia'].choices = lista_parroquia

    parroquia = forms.ChoiceField(
        label=_("Parroquia"),
        widget=forms.Select(attrs={
            'class': 'form-control select2', 'data-toggle': 'tooltip', 'style':'width:250px;',
            'title': _("Seleccione la parroquia"),
        })
    )

    def clean_parroquia(self):
        parroquia = self.cleaned_data['parroquia']
        parroquial = Parroquial.objects.filter(parroquia=parroquia)
        print(parroquial.count())
        if parroquial.count() >= 5:
            raise forms.ValidationError(_("Solo se pueden asignar 5 usuarios para esta parroquia"))

        return parroquia

class ParroquialUpdateForm(PerfilForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ParroquialUpdateForm, self).__init__(*args, **kwargs)
        self.fields['password'].required = False
        self.fields['verificar_contrasenha'].required = False
        self.fields['password'].widget.attrs['disabled'] = True
        self.fields['verificar_contrasenha'].widget.attrs['disabled'] = True
        parroquial = Parroquial.objects.get(perfil=user.perfil)
        lista_parroquia = [('','Selecione...')]
        for pa in Parroquia.objects.filter(municipio=parroquial.parroquia.municipio):
            lista_parroquia.append( (pa.id,pa.nombre) )
        self.fields['parroquia'].choices = lista_parroquia

    parroquia = forms.ChoiceField(
        label=_("Parroquia"),
        widget=forms.Select(attrs={
            'class': 'form-control select2', 'data-toggle': 'tooltip', 'style':'width:250px;',
            'title': _("Seleccione la parroquia"),
        })
    )

    def clean_verificar_contrasenha(self):
        pass

    class Meta:
        model = User
        exclude = [
            'perfil','nivel','password','verificar_contrasenha','date_joined','last_login','is_active',
            'is_superuser','is_staff'
        ]

class ComunalForm(PerfilForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ComunalForm, self).__init__(*args, **kwargs)
        parroquial = Parroquial.objects.get(perfil=user.perfil)
        lista_consejo_comunal = [('','Selecione...')]
        for cc in ConsejoComunal.objects.filter(parroquia=parroquial.parroquia):
            lista_consejo_comunal.append( (cc.rif,cc.rif + ' ' + cc.nombre) )
        self.fields['consejo_comunal'].choices = lista_consejo_comunal

    consejo_comunal = forms.ChoiceField(
        label=_("Consejo Comunal"),
        widget=forms.Select(attrs={
            'class': 'form-control select2', 'data-toggle': 'tooltip', 'style':'width:250px;',
            'title': _("Seleccione el consejo comunal"),
        })
    )

class ComunalUpdateForm(PerfilForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ComunalUpdateForm, self).__init__(*args, **kwargs)
        self.fields['password'].required = False
        self.fields['verificar_contrasenha'].required = False
        self.fields['password'].widget.attrs['disabled'] = True
        self.fields['verificar_contrasenha'].widget.attrs['disabled'] = True
        comunal= Comunal.objects.get(perfil=user.perfil)
        lista_consejo_comunal = [('','Selecione...')]
        for cc in ConsejoComunal.objects.filter(parroquia=comunal.consejo_comunal.parroquia):
            lista_consejo_comunal.append( (cc.rif,cc.rif + ' ' + cc.nombre) )
        self.fields['consejo_comunal'].choices = lista_consejo_comunal

    consejo_comunal = forms.ChoiceField(
        label=_("Consejo Comunal"),
        widget=forms.Select(attrs={
            'class': 'form-control select2', 'data-toggle': 'tooltip', 'style':'width:250px;',
            'title': _("Seleccione el consejo comunal"),
        })
    )

    def clean_verificar_contrasenha(self):
        pass

    class Meta:
        model = User
        exclude = [
            'perfil','nivel','password','verificar_contrasenha','date_joined','last_login','is_active',
            'is_superuser','is_staff'
        ]
