from django.db import models
from django.contrib.auth.models import User
from base.models import Country, State, Municipality, Parish, CommunalCouncil
from django.utils.translation import ugettext_lazy as _
from base.constant import LEVEL, NATIONALITY

class Profile(models.Model):

    phone = models.CharField(
        max_length=15, verbose_name='Teléfono'
    )

    level = models.IntegerField(choices=LEVEL, verbose_name='Nivel')

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name='Usuario'
    )

    def __str__(self):
        return '%s | %s %s' % (self.user.username, self.user.first_name, self.user.last_name)

    class Meta:
        verbose_name = _('Perfil')
        verbose_name_plural = _('Perfiles')

class NationalLevel(models.Model):

    country = models.OneToOneField(
        Country, on_delete=models.CASCADE, verbose_name='País'
    )

    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, verbose_name='Perfil'
    )

    def __str__(self):
        return '%s | %s %s | %s' % (self.profile.user.username, self.profile.user.first_name,
            self.profile.user.last_name, str(self.country))

    class Meta:
        verbose_name = _('Nivel Nacional')
        verbose_name_plural = _('Nivel Nacionales')

class StateLevel(models.Model):

    state = models.OneToOneField(
        State, on_delete=models.CASCADE, verbose_name='Estado'
    )

    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, verbose_name='Perfil'
    )

    def __str__(self):
        return '%s | %s %s | %s' % (self.profile.user.username, self.profile.user.first_name,
        self.profile.user.last_name, str(self.state))

    class Meta:
        verbose_name = _('Nivel Estadal')
        verbose_name_plural = _('Nivel Estadales')

class MunicipalLevel(models.Model):

    municipality = models.OneToOneField(
        Municipality, on_delete=models.CASCADE, verbose_name='Municipio'
    )

    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, verbose_name='Perfil'
    )

    def __str__(self):
        return '%s | %s %s | %s' % (self.profile.user.username, self.profile.user.first_name,
        self.profile.user.last_name, str(self.municipality))

    class Meta:
        verbose_name = _('Nivel Municipal')
        verbose_name_plural = _('Nivel Municipales')

class ParishLevel(models.Model):

    parish = models.ForeignKey(
        Parish, on_delete=models.CASCADE, verbose_name='Parroquia'
    )

    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, verbose_name='Perfil'
    )

    def __str__(self):
        return '%s | %s %s | %s' % (self.profile.user.username, self.profile.user.first_name,
        self.profile.user.last_name, str(self.parish))

    class Meta:
        verbose_name = _('Nivel Parroquial')
        verbose_name_plural = _('Nivel Parroquiales')

class CommunalCouncilLevel(models.Model):

    communal_council = models.OneToOneField(
        CommunalCouncil, on_delete=models.CASCADE, verbose_name='Consejo Comunal'
    )

    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, verbose_name='Perfil'
    )

    def __str__(self):
        return '%s | %s %s | %s' % (self.profile.user.username, self.profile.user.first_name,
        self.profile.user.last_name, str(self.communal_council))

    class Meta:
        verbose_name = _('Nivel Consejo Comunal')
        verbose_name_plural = _('Nivel Consejos Comunales')
