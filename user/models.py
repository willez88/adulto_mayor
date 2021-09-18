from base.models import CommunalCouncil, Country, Municipality, Parish, State
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """!
    Clase que contiene los perfiles

    @author William Páez <wpaez@cenditel.gob.ve> | <paez.william8@gmail.com>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    # Teléfono
    phone = models.CharField('teléfono', max_length=15)

    # Usuario
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name='usuario'
    )

    def __str__(self):
        """!
        Método para representar la clase de forma amigable

        @author William Páez <wpaez@cenditel.gob.ve> |
            <paez.william8@gmail.com>
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve una cadena de caracteres
        """

        return self.user.username + ' | ' + self.user.first_name + ' ' +\
            self.user.last_name

    class Meta:
        """!
        Meta clase del modelo que establece algunas propiedades

        @author William Páez <wpaez@cenditel.gob.ve> |
            <paez.william8@gmail.com>
        """

        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'
        ordering = ['user__username']


class NationalLevel(models.Model):
    """!
    Clase que contiene los niveles nacionales

    @author William Páez <wpaez@cenditel.gob.ve> | <paez.william8@gmail.com>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    country = models.OneToOneField(
        Country, on_delete=models.CASCADE, verbose_name='país'
    )

    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, verbose_name='perfil'
    )

    def __str__(self):
        """!
        Método para representar la clase de forma amigable

        @author William Páez <wpaez@cenditel.gob.ve> |
            <paez.william8@gmail.com>
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve una cadena de caracteres
        """

        username = self.profile.user.username
        first_name = self.profile.user.first_name
        last_name = self.profile.user.last_name
        country = str(self.country)
        return username + ' | ' + first_name + ' ' + last_name + ' | ' +\
            country

    class Meta:
        """!
        Meta clase del modelo que establece algunas propiedades

        @author William Páez <wpaez@cenditel.gob.ve> |
            <paez.william8@gmail.com>
        """

        verbose_name = 'Nivel Nacional'
        verbose_name_plural = 'Nivel Nacionales'
        ordering = ['country']


class StateLevel(models.Model):
    """!
    Clase que contiene los niveles estadales

    @author William Páez <wpaez@cenditel.gob.ve> | <paez.william8@gmail.com>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    state = models.OneToOneField(
        State, on_delete=models.CASCADE, verbose_name='estado'
    )

    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, verbose_name='perfil'
    )

    def __str__(self):
        """!
        Método para representar la clase de forma amigable

        @author William Páez <wpaez@cenditel.gob.ve> |
            <paez.william8@gmail.com>
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve una cadena de caracteres
        """

        username = self.profile.user.username
        first_name = self.profile.user.first_name
        last_name = self.profile.user.last_name
        state = str(self.state)
        return username + ' | ' + first_name + ' ' + last_name + ' | ' + state

    class Meta:
        """!
        Meta clase del modelo que establece algunas propiedades

        @author William Páez <wpaez@cenditel.gob.ve> |
            <paez.william8@gmail.com>
        """

        verbose_name = 'Nivel Estadal'
        verbose_name_plural = 'Nivel Estadales'
        ordering = ['state__name']


class MunicipalLevel(models.Model):
    """!
    Clase que contiene los niveles municipales

    @author William Páez <wpaez@cenditel.gob.ve> | <paez.william8@gmail.com>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    municipality = models.OneToOneField(
        Municipality, on_delete=models.CASCADE, verbose_name='municipio'
    )

    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, verbose_name='perfil'
    )

    def __str__(self):
        """!
        Método para representar la clase de forma amigable

        @author William Páez <wpaez@cenditel.gob.ve> |
            <paez.william8@gmail.com>
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve una cadena de caracteres
        """

        username = self.profile.user.username
        first_name = self.profile.user.first_name
        last_name = self.profile.user.last_name
        municipality = str(self.municipality)
        return username + ' | ' + first_name + ' ' + last_name + ' | ' +\
            municipality

    class Meta:
        """!
        Meta clase del modelo que establece algunas propiedades

        @author William Páez <wpaez@cenditel.gob.ve> |
            <paez.william8@gmail.com>
        """

        verbose_name = 'Nivel Municipal'
        verbose_name_plural = 'Nivel Municipales'
        ordering = ['municipality__name']


class ParishLevel(models.Model):
    """!
    Clase que contiene los niveles parroquiales

    @author William Páez <wpaez@cenditel.gob.ve> | <paez.william8@gmail.com>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    parish = models.ForeignKey(
        Parish, on_delete=models.CASCADE, verbose_name='parroquia'
    )

    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, verbose_name='perfil'
    )

    def __str__(self):
        """!
        Método para representar la clase de forma amigable

        @author William Páez <wpaez@cenditel.gob.ve> |
            <paez.william8@gmail.com>
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve una cadena de caracteres
        """

        username = self.profile.user.username
        first_name = self.profile.user.first_name
        last_name = self.profile.user.last_name
        parish = str(self.parish)
        return username + ' | ' + first_name + ' ' + last_name + ' | ' + parish

    class Meta:
        """!
        Meta clase del modelo que establece algunas propiedades

        @author William Páez <wpaez@cenditel.gob.ve> |
            <paez.william8@gmail.com>
        """

        verbose_name = 'Nivel Parroquial'
        verbose_name_plural = 'Nivel Parroquiales'
        ordering = ['parish__name']


class CommunalCouncilLevel(models.Model):
    """!
    Clase que contiene los niveles consejo comunal

    @author William Páez <wpaez@cenditel.gob.ve> | <paez.william8@gmail.com>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    communal_council = models.OneToOneField(
        CommunalCouncil, on_delete=models.CASCADE,
        verbose_name='consejo comunal'
    )

    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, verbose_name='perfil'
    )

    def __str__(self):
        """!
        Método para representar la clase de forma amigable

        @author William Páez <wpaez@cenditel.gob.ve> |
            <paez.william8@gmail.com>
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve una cadena de caracteres
        """

        username = self.profile.user.username
        first_name = self.profile.user.first_name
        last_name = self.profile.user.last_name
        communal_council = str(self.communal_council)
        return username + ' | ' + first_name + ' ' + last_name + ' | ' +\
            communal_council

    class Meta:
        """!
        Meta clase del modelo que establece algunas propiedades

        @author William Páez <wpaez@cenditel.gob.ve> |
            <paez.william8@gmail.com>
        """

        verbose_name = 'Nivel Consejo Comunal'
        verbose_name_plural = 'Nivel Consejos Comunales'
        ordering = ['communal_council']
