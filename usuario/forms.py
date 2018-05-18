from django import forms
from django.contrib.auth.models import User
from base.models import Pais, Estado, Municipio, Parroquia, ConsejoComunal
from django.utils.translation import ugettext_lazy as _
from django.core import validators
from base.fields import CedulaField
from .models import Nacional, Estadal, Municipal, Parroquial, Comunal

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

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email):
            raise forms.ValidationError(_("El correo ya esta registrado"))
        return email

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

class NacionalUpdateForm(PerfilForm):
    """!
    Clase que contiene el formulario para poder actualizar los datos de un usuario que tiene nivel Nacional

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 04-03-2018
    @version 1.0.0
    """

    def __init__(self, *args, **kwargs):
        """!
        Función que inicializa el formulario

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 04-03-2018
        @version 1.0.0
        """

        super(NacionalUpdateForm, self).__init__(*args, **kwargs)
        self.fields['pais'].required = False
        self.fields['password'].required = False
        self.fields['verificar_contrasenha'].required = False
        self.fields['password'].widget.attrs['disabled'] = True
        self.fields['verificar_contrasenha'].widget.attrs['disabled'] = True

    ## Estado donde se encuentra el usuario
    pais = forms.CharField(
        label=_("País"),
        widget=forms.TextInput(attrs={
            'class': 'form-control input-sm', 'data-toggle': 'tooltip', 'style':'width:250px;', 'readonly':'true',
            'title': _("Indica el nombre del pais"),
        })
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exclude(username=username):
            raise forms.ValidationError(_("El correo ya esta registrado"))
        return email

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
            'is_superuser','is_staff', 'pais'
        ]

class EstadalForm(PerfilForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(EstadalForm, self).__init__(*args, **kwargs)
        nacional = Nacional.objects.get(perfil=user.perfil)
        lista_estado = [('','Selecione...')]
        for es in Estado.objects.filter(pais=nacional.pais):
            lista_estado.append( (es.id,es.nombre) )
        self.fields['estado'].choices = lista_estado

    estado = forms.ChoiceField(
        label=_("Estado"),
        widget=forms.Select(attrs={
            'class': 'form-control select2', 'data-toggle': 'tooltip', 'style':'width:250px;',
            'title': _("Seleccione el estado"),
        })
    )

    def clean_estado(self):
        estado = self.cleaned_data['estado']

        if Estadal.objects.filter(estado=estado):
            raise forms.ValidationError(_("Ya existe un usuario asignado a este estado"))

        return estado

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
        self.fields['estado'].required = False
        self.fields['password'].required = False
        self.fields['verificar_contrasenha'].required = False
        self.fields['password'].widget.attrs['disabled'] = True
        self.fields['verificar_contrasenha'].widget.attrs['disabled'] = True

    ## Estado donde se encuentra el usuario
    estado = forms.CharField(
        label=_("Estado"),
        widget=forms.TextInput(attrs={
            'class': 'form-control input-sm', 'data-toggle': 'tooltip', 'style':'width:250px;', 'readonly': 'true',
            'title': _("Indica el nombre del estado"),
        })
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exclude(username=username):
            raise forms.ValidationError(_("El correo ya esta registrado"))
        return email

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
            'is_superuser','is_staff','estado'
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
        self.fields['municipio'].required = False
        self.fields['password'].required = False
        self.fields['verificar_contrasenha'].required = False
        self.fields['password'].widget.attrs['disabled'] = True
        self.fields['verificar_contrasenha'].widget.attrs['disabled'] = True

    municipio = forms.CharField(
        label=_("Municipio"),
        widget=forms.TextInput(attrs={
            'class': 'form-control input-sm', 'data-toggle': 'tooltip', 'style':'width:250px;', 'readonly': 'true',
            'title': _("Indica el nombre del municipio"),
        })
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exclude(username=username):
            raise forms.ValidationError(_("El correo ya esta registrado"))
        return email

    def clean_verificar_contrasenha(self):
        pass

    class Meta:
        model = User
        exclude = [
            'perfil','nivel','password','verificar_contrasenha','date_joined','last_login','is_active',
            'is_superuser','is_staff','municipio'
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
        self.fields['parroquia'].required = False
        self.fields['password'].required = False
        self.fields['verificar_contrasenha'].required = False
        self.fields['password'].widget.attrs['disabled'] = True
        self.fields['verificar_contrasenha'].widget.attrs['disabled'] = True

    parroquia = forms.CharField(
        label=_("Parroquia"),
        widget=forms.TextInput(attrs={
            'class': 'form-control input-sm', 'data-toggle': 'tooltip', 'style':'width:250px;', 'readonly': 'true',
            'title': _("Indica el nombre de la parroquia"),
        })
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exclude(username=username):
            raise forms.ValidationError(_("El correo ya esta registrado"))
        return email

    def clean_verificar_contrasenha(self):
        pass

    class Meta:
        model = User
        exclude = [
            'perfil','nivel','password','verificar_contrasenha','date_joined','last_login','is_active',
            'is_superuser','is_staff','parroquia'
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
        self.fields['consejo_comunal'].required = False
        self.fields['password'].required = False
        self.fields['verificar_contrasenha'].required = False
        self.fields['password'].widget.attrs['disabled'] = True
        self.fields['verificar_contrasenha'].widget.attrs['disabled'] = True

    consejo_comunal = forms.CharField(
        label=_("Consejo Comunal"),
        widget=forms.TextInput(attrs={
            'class': 'form-control input-sm', 'data-toggle': 'tooltip', 'style':'width:250px;', 'readonly': 'true',
            'title': _("Indica el nombre del consejo comunal"),
        })
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exclude(username=username):
            raise forms.ValidationError(_("El correo ya esta registrado"))
        return email

    def clean_verificar_contrasenha(self):
        pass

    class Meta:
        model = User
        exclude = [
            'perfil','nivel','password','verificar_contrasenha','date_joined','last_login','is_active',
            'is_superuser','is_staff','consejo_comunal'
        ]
