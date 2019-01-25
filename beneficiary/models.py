from django.db import models
from base.models import (
    Gender,MaritalStatus,InstructionDegree,EducationalMission,SocialMission,IncomeType,
    Disease,Disability,CommunalCouncil
)
from user.models import CommunalCouncilLevel
from django.utils.translation import ugettext_lazy as _
import datetime

# Create your models here.

class Person(models.Model):
    """!
    Clase que contiene los datos de las personas adultas mayores

    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://conocimientolibre.cenditel.gob.ve/licencia-de-software-v-1-3/'>Licencia de Software CENDITEL versión 1.2</a>
    """

    ## Nombre de la Persona
    first_name = models.CharField(max_length=100)

    ## Apellido de la Persona
    last_name = models.CharField(max_length=100)

    ## Cédula de la Persona. Si tiene o no
    identity_card = models.CharField(
        max_length=9,
        unique=True,
        null=True
    )

    # +58-416-0708340
    phone = models.CharField(
        max_length=15,
    )

    ## Establece el correo de la persona
    email = models.CharField(
        max_length=100, help_text=('correo@correo.com'), unique=True, null=True
    )

    ## Establece el sexo de la Persona
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)

    ## Establece la fecha de nacimiento de la Persona
    birthdate = models.DateField()

    ## Establece el Estado Civil de la Persona
    marital_status = models.ForeignKey(MaritalStatus, on_delete=models.CASCADE)

    ## Establece el Grado de Instrucción de la Persona
    instruction_degree = models.ForeignKey(InstructionDegree, on_delete=models.CASCADE)

    ## Establece la Misión Educativa que tiene la Persona
    educational_mission = models.ForeignKey(EducationalMission, on_delete=models.CASCADE)

    ## Establece la Misión Social que tiene la Persona
    social_mission = models.ForeignKey(SocialMission, on_delete=models.CASCADE)

    ## Establece los ingresos de dinero de la Persona
    income_type = models.ForeignKey(IncomeType, on_delete=models.CASCADE)

    ## Establece si la persona tiene o no ingresos por ser pensionado
    pensioner = models.BooleanField()

    ## Establece si la persona tiene o no ingresos por ser jubilado
    retired = models.BooleanField()

    ## Establece la Enfermedad que presenta la Persona
    diseases = models.ManyToManyField(Disease, blank=True)

    ## Establece la Discapacidad que tiene la Persona
    disabilities = models.ManyToManyField(Disability, blank=True)

    ## Establece la relación de la Persona con un usuario del sistema
    communal_council_level = models.ForeignKey(CommunalCouncilLevel,on_delete=models.CASCADE)

    ## Cacula la edad en años que tiene una persona según su fecha de nacimiento
    def age(self):
        """!
        Método que calcula la edad de la persona

        @author William Páez (wpaez at cenditel.gob.ve)
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna un número entero que representa la edad
        """

        return int((datetime.date.today() - self.birthdate).days / 365.25  )

    def __str__(self):
        """!
        Método para representar la clase de forma amigable

        @author William Páez (wpaez at cenditel.gob.ve)
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve una cadena de caracteres con el nombre, apellido y cédula de la persona
        """

        return self.first_name + ' ' + self.last_name + ' | ' + str(self.identity_card)

    class Meta:
        verbose_name = _('Persona')
        verbose_name_plural = _('Personas')
