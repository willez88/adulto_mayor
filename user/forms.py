from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core import validators
from base.fields import IdentityCardField, PhoneField
from .models import Profile, NationalLevel, StateLevel, MunicipalLevel, ParishLevel, CommunalCouncilLevel
from base.models import State, Municipality, Parish, CommunalCouncil

class ProfileForm(forms.ModelForm):
    """!
    Clase que contiene los campos del formulario de perfil del usuario

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 14-01-2018
    @version 1.0.0
    """

    ## Username para identificar al usuario, en este caso se usa la cédula
    username = IdentityCardField(
        validators=[
            validators.RegexValidator(
                r'^[VE][\d]{8}$',
                _('Introduzca un número de cédula válido. Solo se permiten números y una longitud de 8 carácteres. Se agregan ceros (0) si la longitud es de 7 o menos caracteres.')
            ),
        ],
    )

    ## Nombres del usuario
    first_name = forms.CharField(
        label=_('Nombres:'), max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip',
                'title': _('Indique los Nombres.'),
            }
        )
    )

    ## Apellidos del usuario
    last_name = forms.CharField(
        label=_('Apellidos:'), max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip',
                'title': _('Indique los Apellidos.'),
            }
        )
    )

    ## Correo del usuario
    email = forms.EmailField(
        label=_('Correo Electrónico:'), max_length=100,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control input-sm email-mask', 'data-toggle': 'tooltip',
                'title': _('Indique el correo electrónico de contacto.')
            }
        )
    )

    ## Teléfono del usuario
    phone = PhoneField(
        validators=[
            validators.RegexValidator(
                r'^\+\d{2}-\d{3}-\d{7}$',
                _('Número telefónico inválido. Debe tener el formato que aparece en la ayuda.')
            ),
        ],
    )

    ## Clave de acceso del usuario
    password = forms.CharField(
        label=_('Contraseña:'), max_length=128,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip',
                'title': _('Indique una contraseña de aceso al sistema.')
            }
        )
    )

    ## Confirmación de clave de acceso del usuario
    confirm_password = forms.CharField(
        label=_('Confirmar Contraseña:'), max_length=128,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control input-sm', 'data-toggle': 'tooltip',
                'title': _('Indique nuevamente la contraseña de aceso al sistema.')
            }
        )
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email):
            raise forms.ValidationError(_('El correo ya esta registrado.'))
        return email

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data['confirm_password']
        password = self.cleaned_data.get('password')
        if password != confirm_password:
            raise forms.ValidationError(_('La contraseña no es la misma.'))
        return confirm_password

class NationalLevelUpdateForm(ProfileForm):
    """!
    Clase que contiene el formulario para poder actualizar los datos de un usuario que tiene nivel Nacional

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 04-03-2018
    @version 1.0.0
    """

    def __init__(self, *args, **kwargs):
        """!
        Función que inicializa el formulario

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 04-03-2018
        @version 1.0.0
        """

        super(NationalLevelUpdateForm, self).__init__(*args, **kwargs)
        self.fields['country'].required = False
        self.fields['password'].required = False
        self.fields['confirm_password'].required = False
        self.fields['password'].widget.attrs['disabled'] = True
        self.fields['confirm_password'].widget.attrs['disabled'] = True

    ## Estado donde se encuentra el usuario
    country = forms.CharField(
        label=_('País:'),
        widget=forms.TextInput(attrs={
            'class': 'form-control input-sm', 'data-toggle': 'tooltip', 'readonly':'true',
            'title': _('Indica el nombre del país.'),
        })
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exclude(username=username):
            raise forms.ValidationError(_('El correo ya esta registrado.'))
        return email

    def clean_confirm_password(self):
        pass

    class Meta:
        """!
        Meta clase del formulario que establece algunas propiedades

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        model = Profile
        fields = [
            'username','first_name','last_name','email','phone','password','confirm_password',
        ]

class StateLevelForm(ProfileForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(StateLevelForm, self).__init__(*args, **kwargs)
        national_level = NationalLevel.objects.get(profile=user.profile)
        list_state = [('','Selecione...')]
        for st in State.objects.filter(country=national_level.country):
            list_state.append( (st.id,st) )
        self.fields['state'].choices = list_state

    state = forms.ChoiceField(
        label=_('Estado:'),
        widget=forms.Select(attrs={
            'class': 'form-control select2', 'data-toggle': 'tooltip',
            'title': _('Seleccione el estado.'),
        })
    )

    def clean_state(self):
        state = self.cleaned_data['state']
        if StateLevel.objects.filter(state=state):
            raise forms.ValidationError(_('Ya existe un usuario asignado a este estado.'))
        return state

    class Meta:
        """!
        Meta clase del formulario que establece algunas propiedades

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        """

        model = User
        fields = [
            'username','first_name','last_name','email','phone','password','confirm_password',
        ]

class StateLevelUpdateForm(ProfileForm):
    """!
    Clase que contiene el formulario para poder actualizar los datos de un usuario que tiene nivel estadal

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 14-01-2018
    @version 1.0.0
    """

    def __init__(self, *args, **kwargs):
        """!
        Función que inicializa el formulario

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        super(StateLevelUpdateForm, self).__init__(*args, **kwargs)
        self.fields['state'].required = False
        self.fields['password'].required = False
        self.fields['confirm_password'].required = False
        self.fields['password'].widget.attrs['disabled'] = True
        self.fields['confirm_password'].widget.attrs['disabled'] = True

    ## Estado donde se encuentra el usuario
    state = forms.CharField(
        label=_('Estado:'),
        widget=forms.TextInput(attrs={
            'class': 'form-control input-sm', 'data-toggle': 'tooltip', 'readonly': 'true',
            'title': _('Indica el nombre del estado.'),
        })
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exclude(username=username):
            raise forms.ValidationError(_('El correo ya esta registrado.'))
        return email

    def clean_confirm_password(self):
        pass

    class Meta:
        """!
        Meta clase del formulario que establece algunas propiedades

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        model = Profile
        fields = [
            'username','first_name','last_name','email','phone','password','confirm_password',
        ]

class MunicipalLevelForm(ProfileForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(MunicipalLevelForm, self).__init__(*args, **kwargs)
        state_level = StateLevel.objects.get(profile=user.profile)
        list_municipality = [('','Selecione...')]
        for mu in Municipality.objects.filter(state=state_level.state):
            list_municipality.append( (mu.id,mu) )
        self.fields['municipality'].choices = list_municipality

    municipality = forms.ChoiceField(
        label=_('Municipio:'),
        widget=forms.Select(attrs={
            'class': 'form-control select2', 'data-toggle': 'tooltip',
            'title': _('Seleccione el municipio.'),
        })
    )

    def clean_municipality(self):
        municipality = self.cleaned_data['municipality']
        if MunicipalLevel.objects.filter(municipality=municipality):
            raise forms.ValidationError(_('Ya existe un usuario asignado a este municipio.'))
        return municipality

    class Meta:
        """!
        Meta clase del formulario que establece algunas propiedades

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        """

        model = User
        fields = [
            'username','first_name','last_name','email','phone','password','confirm_password',
        ]

class MunicipalLevelUpdateForm(ProfileForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(MunicipalLevelUpdateForm, self).__init__(*args, **kwargs)
        self.fields['municipality'].required = False
        self.fields['password'].required = False
        self.fields['confirm_password'].required = False
        self.fields['password'].widget.attrs['disabled'] = True
        self.fields['confirm_password'].widget.attrs['disabled'] = True

    municipality = forms.CharField(
        label=_('Municipio:'),
        widget=forms.TextInput(attrs={
            'class': 'form-control input-sm', 'data-toggle': 'tooltip', 'readonly': 'true',
            'title': _('Indica el nombre del municipio.'),
        })
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exclude(username=username):
            raise forms.ValidationError(_('El correo ya esta registrado.'))
        return email

    def clean_verificar_contrasenha(self):
        pass

    class Meta:
        model = Profile
        fields = [
            'username','first_name','last_name','email','phone','password','confirm_password',
        ]

class ParishLevelForm(ProfileForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ParishLevelForm, self).__init__(*args, **kwargs)
        municipal_level = MunicipalLevel.objects.get(profile=user.profile)
        list_parish = [('','Selecione...')]
        for pa in Parish.objects.filter(municipality=municipal_level.municipality):
            list_parish.append( (pa.id,pa) )
        self.fields['parish'].choices = list_parish

    parish = forms.ChoiceField(
        label=_('Parroquia:'),
        widget=forms.Select(attrs={
            'class': 'form-control select2', 'data-toggle': 'tooltip',
            'title': _('Seleccione la parroquia.'),
        })
    )

    def clean_parish(self):
        parish = self.cleaned_data['parish']
        parish_level = ParishLevel.objects.filter(parish=parish)
        if parish_level.count() >= 5:
            raise forms.ValidationError(_('Solo se pueden asignar 5 usuarios para esta parroquia.'))
        return parish

    class Meta:
        """!
        Meta clase del formulario que establece algunas propiedades

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        """

        model = User
        fields = [
            'username','first_name','last_name','email','phone','password','confirm_password',
        ]

class ParishLevelUpdateForm(ProfileForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ParishLevelUpdateForm, self).__init__(*args, **kwargs)
        self.fields['parish'].required = False
        self.fields['password'].required = False
        self.fields['confirm_password'].required = False
        self.fields['password'].widget.attrs['disabled'] = True
        self.fields['confirm_password'].widget.attrs['disabled'] = True

    parish = forms.CharField(
        label=_('Parroquia:'),
        widget=forms.TextInput(attrs={
            'class': 'form-control input-sm', 'data-toggle': 'tooltip', 'readonly': 'true',
            'title': _('Indica el nombre de la parroquia.'),
        })
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exclude(username=username):
            raise forms.ValidationError(_('El correo ya esta registrado.'))
        return email

    def clean_confirm_password(self):
        pass

    class Meta:
        model = Profile
        fields = [
            'username','first_name','last_name','email','phone','password','confirm_password',
        ]

class CommunalCouncilLevelAdminForm(forms.ModelForm):

    ## Estado donde se ecnuetra ubicado el municipio
    state = forms.ModelChoiceField(
        label=_('Estado:'), queryset=State.objects.all(), empty_label=_('Seleccione...'),
        widget=forms.Select(attrs={
            'class': 'form-control select2', 'data-toggle': 'tooltip',
            'title': _('Seleccione el estado en donde se encuentra ubicada.'),
        })
    )

    ## Municipio donde se encuentra ubicada la parroquia
    municipality = forms.ModelChoiceField(
        label=_('Municipio:'), queryset=Municipality.objects.all(), empty_label=_('Seleccione...'),
        widget=forms.Select(attrs={
            'class': 'form-control select2', 'data-toggle': 'tooltip', 'disabled': 'true',
            'title': _('Seleccione el municipio en donde se encuentra ubicada.'),
        })
    )

    ## Parroquia donde se encuentra ubicado el consejo comunal
    parish = forms.ModelChoiceField(
        label=_('Parroquia:'), queryset=Parish.objects.all(), empty_label=_('Seleccione...'),
        widget=forms.Select(attrs={
            'class': 'form-control select2', 'data-toggle': 'tooltip', 'disabled': 'true',
            'title': _('Seleccione la parroquia en donde se encuentra ubicada.'),
        })
    )

    class Meta:

        model = User
        fields = '__all__'

class CommunalCouncilLevelForm(ProfileForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(CommunalCouncilLevelForm, self).__init__(*args, **kwargs)
        parish_level = ParishLevel.objects.get(profile=user.profile)
        list_communal_council = [('','Selecione...')]
        for cc in CommunalCouncil.objects.filter(parish=parish_level.parish):
            list_communal_council.append( (cc.rif,cc) )
        self.fields['communal_council'].choices = list_communal_council

    communal_council = forms.ChoiceField(
        label=_('Consejo Comunal:'),
        widget=forms.Select(attrs={
            'class': 'form-control select2', 'data-toggle': 'tooltip',
            'title': _('Seleccione el consejo comunal.'),
        })
    )

    class Meta:
        """!
        Meta clase del formulario que establece algunas propiedades

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
        """

        model = User
        fields = [
            'username','first_name','last_name','email','phone','password','confirm_password',
        ]

class CommunalCouncilLevelUpdateForm(ProfileForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(CommunalCouncilLevelUpdateForm, self).__init__(*args, **kwargs)
        self.fields['communal_council'].required = False
        self.fields['password'].required = False
        self.fields['confirm_password'].required = False
        self.fields['password'].widget.attrs['disabled'] = True
        self.fields['confirm_password'].widget.attrs['disabled'] = True

    communal_council = forms.CharField(
        label=_('Consejo Comunal:'),
        widget=forms.TextInput(attrs={
            'class': 'form-control input-sm', 'data-toggle': 'tooltip', 'readonly': 'true',
            'title': _('Indica el nombre del consejo comunal.'),
        })
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exclude(username=username):
            raise forms.ValidationError(_('El correo ya esta registrado.'))
        return email

    def clean_confirm_password(self):
        pass

    class Meta:
        model = Profile
        fields = [
            'username','first_name','last_name','email','phone','password','confirm_password',
        ]
