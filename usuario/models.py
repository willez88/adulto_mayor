from django.db import models
from django.contrib.auth.models import User
from base.models import Estado, Municipio, Parroquia
from django.utils.translation import ugettext_lazy as _
from base.constant import NIVEL, NACIONALIDAD
from base.fields import CedulaField

# Create your models here.

class Perfil(models.Model):

    telefono = models.CharField(
        max_length=15,
    )

    nivel = models.IntegerField(choices=NIVEL)

    user = models.OneToOneField(
        User, related_name="perfil",
        help_text=_("Relación entre los datos de registro y el usuario con acceso al sistema"),
        on_delete=models.CASCADE
    )

    def __str__(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)

    class Meta:
        verbose_name = _("Perfil")
        verbose_name_plural = _("Perfiles")

class Estadal(models.Model):

    estado = models.OneToOneField(
        Estado, on_delete=models.CASCADE
    )

    perfil = models.OneToOneField(
        Perfil, on_delete=models.CASCADE
    )

    def __str__(self):
        return "%s %s" % (self.perfil.user.first_name, self.perfil.user.last_name)

    class Meta:
        verbose_name = _("Estadal")
        verbose_name_plural = _("Estadales")

class Municipal(models.Model):

    municipio = models.OneToOneField(
        Municipio, on_delete=models.CASCADE
    )

    perfil = models.OneToOneField(
        Perfil, on_delete=models.CASCADE
    )

    def __str__(self):
        return "%s %s" % (self.perfil.user.first_name, self.perfil.user.last_name)

    class Meta:
        verbose_name = _("Municipal")
        verbose_name_plural = _("Municipales")

class Parroquial(models.Model):

    parroquia = models.OneToOneField(
        Parroquia, on_delete=models.CASCADE
    )

    perfil = models.OneToOneField(
        Perfil, on_delete=models.CASCADE
    )

    def __str__(self):
        return "%s %s" % (self.perfil.user.first_name, self.perfil.user.last_name)

    class Meta:
        verbose_name = _("Parroquial")
        verbose_name_plural = _("Parroquiales")
