import datetime

from base.models import (
    Disability, Disease, EducationalMission, Gender, IncomeType,
    InstructionDegree, MaritalStatus, SocialMission,
)
from django.db import models
from user.models import CommunalCouncilLevel


class Person(models.Model):
    """!
    Clase que contiene los datos de las personas adultas mayores

    @author William Páez <paez.william8@gmail.com>
    @copyright <a href='​http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    # Nombre de la Persona
    first_name = models.CharField('nombre', max_length=100)

    # Apellido de la Persona
    last_name = models.CharField('apellido', max_length=100)

    # Cédula de la Persona. Si tiene o no
    identity_card = models.CharField(
        'cédula de identidad',
        max_length=9,
        unique=True,
        null=True
    )

    # +58-416-0708340
    phone = models.CharField(
        max_length=15,
    )

    # Establece el correo de la persona
    email = models.CharField(
        'correo eléctronico', max_length=100, help_text='correo@correo.com',
        unique=True, null=True
    )

    # Establece el género
    gender = models.ForeignKey(
        Gender, on_delete=models.CASCADE, verbose_name='género'
    )

    # Establece la fecha de nacimiento de la Persona
    birthdate = models.DateField('fecha de nacimiento')

    # Establece el Estado Civil de la Persona
    marital_status = models.ForeignKey(
        MaritalStatus, on_delete=models.CASCADE, verbose_name='estado civil'
    )

    # Establece el Grado de Instrucción de la Persona
    instruction_degree = models.ForeignKey(
        InstructionDegree, on_delete=models.CASCADE, null=True, blank=True,
        verbose_name='grado de instrucción'
    )

    # Establece la Misión Educativa que tiene la Persona
    educational_mission = models.ForeignKey(
        EducationalMission, on_delete=models.CASCADE, null=True, blank=True,
        verbose_name='misión educativa'
    )

    # Establece la Misión Social que tiene la Persona
    social_mission = models.ForeignKey(
        SocialMission, on_delete=models.CASCADE, null=True, blank=True,
        verbose_name='misión social'
    )

    # Establece los ingresos de dinero de la Persona
    income_type = models.ForeignKey(
        IncomeType, on_delete=models.CASCADE, null=True, blank=True,
        verbose_name='tipo de ingreso'
    )

    # Establece si la persona tiene o no ingresos por ser pensionado
    pensioner = models.BooleanField('pensionado')

    # Establece si la persona tiene o no ingresos por ser jubilado
    retired = models.BooleanField('retirado')

    # Establece la Enfermedad que presenta la Persona
    diseases = models.ManyToManyField(
        Disease, blank=True, verbose_name='enfermedades'
    )

    # Establece la Discapacidad que tiene la Persona
    disabilities = models.ManyToManyField(
        Disability, blank=True, verbose_name='discapacidades'
    )

    # Establece la relación de la Persona con un usuario del sistema
    communal_council_level = models.ForeignKey(
        CommunalCouncilLevel, on_delete=models.CASCADE,
        verbose_name='nivel consejo comunal', null=True
    )

    def age(self):
        """!
        Método que calcula la edad de la persona

        @author William Páez <paez.william8@gmail.com>
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna un número entero que representa la edad
        """

        return int((datetime.date.today() - self.birthdate).days / 365.25)

    def __str__(self):
        """!
        Método para representar la clase de forma amigable

        @author William Páez <paez.william8@gmail.com>
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve una cadena de caracteres
        """

        return self.first_name + ' ' + self.last_name + ' | ' +\
            str(self.identity_card)

    class Meta:
        """!
        Meta clase del modelo que establece algunas propiedades

        @author William Páez <paez.william8@gmail.com>
        """

        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'
