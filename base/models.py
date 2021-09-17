from django.core import validators
from django.db import models


class Country(models.Model):
    """!
    Clase que contiene los paises

    @author Ing. Roldan Vargas <rvargas@cenditel.gob.ve>
    @author William Páez <wpaez@cenditel.gob.ve> | <paez.william8@gmail.com>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    # Nombre del país
    name = models.CharField(max_length=80)

    def __str__(self):
        """!
        Método para representar la clase de forma amigable

        @author William Páez <wpaez@cenditel.gob.ve> |
            <paez.william8@gmail.com>
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve una cadena de caracteres
        """

        return self.name


class State(models.Model):
    """!
    Clase que contiene los estados

    @author Ing. Roldan Vargas <rvargas@cenditel.gob.ve>
    @author William Páez <wpaez@cenditel.gob.ve> | <paez.william8@gmail.com>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    # Nombre del Estado
    name = models.CharField(max_length=50)

    # Establece la relación del estado con el país
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        """!
        Método para representar la clase de forma amigable

        @author William Páez <wpaez@cenditel.gob.ve> |
            <paez.william8@gmail.com>
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve una cadena de caracteres
        """

        return self.name


class Municipality(models.Model):
    """!
    Clase que contiene los municipios

    @author Ing. Roldan Vargas <rvargas@cenditel.gob.ve>
    @author William Páez <wpaez@cenditel.gob.ve> | <paez.william8@gmail.com>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    # Nombre del Municipio
    name = models.CharField(max_length=50)

    # Establece la relación del municipio con el estado
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        """!
        Método para representar la clase de forma amigable

        @author William Páez <wpaez@cenditel.gob.ve> |
            <paez.william8@gmail.com>
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve una cadena de caracteres
        """

        return self.name


class City(models.Model):
    """!
    Clase que contiene las ciudades

    @author Ing. Roldan Vargas <rvargas@cenditel.gob.ve>
    @author William Páez <wpaez@cenditel.gob.ve> | <paez.william8@gmail.com>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    # Nombre de la Ciudad
    name = models.CharField(max_length=50)

    # Establece la relación de la ciudad con el estado
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        """!
        Método para representar la clase de forma amigable

        @author William Páez <wpaez@cenditel.gob.ve> |
            <paez.william8@gmail.com>
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve una cadena de caracteres
        """

        return self.name


class Parish(models.Model):
    """!
    Clase que contiene las parroquias

    @author Ing. Roldan Vargas <rvargas@cenditel.gob.ve>
    @author William Páez <wpaez@cenditel.gob.ve> | <paez.william8@gmail.com>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    # Nombre de la Parroquia
    name = models.CharField(max_length=50)

    # Establece la relación de la parroquia con el municipio
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE)

    def __str__(self):
        """!
        Método para representar la clase de forma amigable

        @author William Páez <wpaez@cenditel.gob.ve> |
            <paez.william8@gmail.com>
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve una cadena de caracteres
        """

        return self.name


class CommunalCouncil(models.Model):
    """!
    Clase que contiene los consejos comunales

    @author William Páez <wpaez@cenditel.gob.ve> | <paez.william8@gmail.com>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    # Número de rif del consejo comunal
    rif = models.CharField(
        max_length=10, help_text='Rif del Consejo Comunal',
        validators=[
            validators.RegexValidator(
                r'^C[\d]{9}$',
                'Introduzca un rif válido. Solo se permite la letra C y 9 \
                números.'
            ),
        ],
        primary_key=True
    )

    # Nombre del Consejo Comunal
    name = models.CharField('nombre', max_length=500)

    # Establece la relación del consejo comunal con la parroquia
    parish = models.ForeignKey(
        Parish, on_delete=models.CASCADE, verbose_name='parroquia'
    )

    def __str__(self):
        """!
        Método para representar la clase de forma amigable

        @author William Páez <wpaez@cenditel.gob.ve> |
            <paez.william8@gmail.com>
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve una cadena de caracteres
            comunal
        """

        return self.name

    class Meta:
        """!
        Meta clase del modelo que establece algunas propiedades

        @author William Páez <wpaez@cenditel.gob.ve> |
            <paez.william8@gmail.com>
        """

        verbose_name = 'Consejo Comunal'
        verbose_name_plural = 'Consejos Comunales'


class MaritalStatus(models.Model):
    """!
    Clase que contiene los estados civiles

    @author William Páez <wpaez@cenditel.gob.ve> | <paez.william8@gmail.com>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    # Nombre
    name = models.CharField('nombre', max_length=30)

    def __str__(self):
        """!
        Método para representar la clase de forma amigable

        @author William Páez <wpaez@cenditel.gob.ve> |
            <paez.william8@gmail.com>
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve una cadena de caracteres
        """

        return self.name

    class Meta:
        """!
        Meta clase del modelo que establece algunas propiedades

        @author William Páez <wpaez@cenditel.gob.ve> |
            <paez.william8@gmail.com>
        """

        verbose_name = 'Estado Civil'
        verbose_name_plural = 'Estados Civiles'
        ordering = ('name',)


class InstructionDegree(models.Model):
    """!
    Clase que contiene los estados civiles

    @author William Páez <wpaez@cenditel.gob.ve> | <paez.william8@gmail.com>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    # Nombre
    name = models.CharField('nombre', max_length=50)

    def __str__(self):
        """!
        Método para representar la clase de forma amigable

        @author William Páez <wpaez@cenditel.gob.ve> |
            <paez.william8@gmail.com>
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve una cadena de caracteres
        """

        return self.name

    class Meta:
        """!
        Meta clase del modelo que establece algunas propiedades

        @author William Páez <wpaez@cenditel.gob.ve> |
            <paez.william8@gmail.com>
        """

        verbose_name = 'Grado de Instrucción'
        verbose_name_plural = 'Grados de Instrucción'
        ordering = ('name',)


class EducationalMission(models.Model):
    """!
    Clase que contiene las misiones educativas

    @author William Páez <wpaez@cenditel.gob.ve> | <paez.william8@gmail.com>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    # Nombre
    name = models.CharField('nombre', max_length=50)

    def __str__(self):
        """!
        Método para representar la clase de forma amigable

        @author William Páez <wpaez@cenditel.gob.ve> |
            <paez.william8@gmail.com>
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve una cadena de caracteres
        """

        return self.name

    class Meta:
        """!
        Meta clase del modelo que establece algunas propiedades

        @author William Páez <wpaez@cenditel.gob.ve> |
            <paez.william8@gmail.com>
        """

        verbose_name = 'Misión Educativa'
        verbose_name_plural = 'Misiones Educativas'
        ordering = ('name',)


class SocialMission(models.Model):
    """!
    Clase que contiene las misiones sociales

    @author William Páez <wpaez@cenditel.gob.ve> | <paez.william8@gmail.com>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    # Nombre
    name = models.CharField('nombre', max_length=50)

    def __str__(self):
        """!
        Método para representar la clase de forma amigable

        @author William Páez <wpaez@cenditel.gob.ve> |
            <paez.william8@gmail.com>
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve una cadena de caracteres
        """

        return self.name

    class Meta:
        """!
        Meta clase del modelo que establece algunas propiedades

        @author William Páez <wpaez@cenditel.gob.ve> |
            <paez.william8@gmail.com>
        """

        verbose_name = 'Misión Social'
        verbose_name_plural = 'Misiones Sociales'
        ordering = ('name',)


class IncomeType(models.Model):
    """!
    Clase que contiene los tipos de ingreso

    @author William Páez <wpaez@cenditel.gob.ve> | <paez.william8@gmail.com>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    # Nombre
    name = models.CharField('nombre', max_length=50)

    def __str__(self):
        """!
        Método para representar la clase de forma amigable

        @author William Páez <wpaez@cenditel.gob.ve> |
            <paez.william8@gmail.com>
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve una cadena de caracteres
        """

        return self.name

    class Meta:
        """!
        Meta clase del modelo que establece algunas propiedades

        @author William Páez <wpaez@cenditel.gob.ve> |
            <paez.william8@gmail.com>
        """

        verbose_name = 'Tipo de Ingreso'
        verbose_name_plural = 'Tipos de Ingreso'
        ordering = ('name',)


class Gender(models.Model):
    """!
    Clase que contiene los géneros

    @author William Páez <wpaez@cenditel.gob.ve> | <paez.william8@gmail.com>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    # Nombre
    name = models.CharField('nombre', max_length=20)

    def __str__(self):
        """!
        Método para representar la clase de forma amigable

        @author William Páez <wpaez@cenditel.gob.ve> |
            <paez.william8@gmail.com>
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve una cadena de caracteres
        """

        return self.name

    class Meta:
        """!
        Meta clase del modelo que establece algunas propiedades

        @author William Páez <wpaez@cenditel.gob.ve> |
            <paez.william8@gmail.com>
        """

        verbose_name = 'Género'
        verbose_name_plural = 'Géneros'
        ordering = ('name',)


class Disease(models.Model):
    """!
    Clase que contiene las enfermedades

    @author William Páez <wpaez@cenditel.gob.ve> | <paez.william8@gmail.com>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    # Nombre
    name = models.CharField('nombre', max_length=150)

    def __str__(self):
        """!
        Método para representar la clase de forma amigable

        @author William Páez <wpaez@cenditel.gob.ve> |
            <paez.william8@gmail.com>
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Devuelve una cadena de caracteres
        """

        return self.name

    class Meta:
        """!
        Meta clase del modelo que establece algunas propiedades

        @author William Páez <wpaez@cenditel.gob.ve> |
            <paez.william8@gmail.com>
        """

        verbose_name = 'Enfermedad'
        verbose_name_plural = 'Enfermedades'
        ordering = ('name',)


class Disability(models.Model):
    """!
    Clase que contiene las discapacidades

    @author William Páez <wpaez@cenditel.gob.ve> | <paez.william8@gmail.com>
    @copyright <a href='https://tinyurl.com/y3tfnema'>
        Licencia de Software CENDITEL versión 1.2</a>
    """

    # Nombre
    name = models.CharField('nombre', max_length=150)

    def __str__(self):
        """!
        Meta clase del modelo que establece algunas propiedades

        @author William Páez <wpaez@cenditel.gob.ve> |
            <paez.william8@gmail.com>
        """

        return self.name

    class Meta:
        """!
        Meta clase del modelo que establece algunas propiedades

        @author William Páez <wpaez@cenditel.gob.ve> |
            <paez.william8@gmail.com>
        """

        verbose_name = 'Discapacidad'
        verbose_name_plural = 'Discapacidades'
        ordering = ('name',)
