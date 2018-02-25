from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class Pais(models.Model):
    """!
    Clase que contiene los paises

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve) / William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 14-01-2018
    @version 1.0.0
    """

    ## Nombre del pais
    nombre = models.CharField(max_length=80)

    def __str__(self):
        """!
        Función para representar la clase de forma amigable

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        return self.nombre

class Estado(models.Model):
    """!
    Clase que contiene los estados que se encuentran en un país

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve) / William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 14-01-2018
    @version 1.0.0
    """

    ## Nombre del Estado
    nombre = models.CharField(max_length=50)

    ## Pais en donde esta ubicado el Estado
    pais = models.ForeignKey(Pais,on_delete=models.CASCADE)

    def __str__(self):
        """!
        Función para representar la clase de forma amigable

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        return self.nombre

class Municipio(models.Model):
    """!
    Clase que contiene los municipios que se encuentran en un estado

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve) / William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 14-01-2018
    @version 1.0.0
    """

    ## Nombre del Municipio
    nombre = models.CharField(max_length=50)

    ## Estado en donde se encuentra el Municipio
    estado = models.ForeignKey(Estado,on_delete=models.CASCADE)

    def __str__(self):
        """!
        Función para representar la clase de forma amigable

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        return self.nombre

class Ciudad(models.Model):
    """!
    Clase que contiene las ciudades que se encuentran en un estado

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve) / William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 14-01-2018
    @version 1.0.0
    """

    ## Nombre de la Ciudad
    nombre = models.CharField(max_length=50)

    ## Estado en donde se encuentra ubicada la Ciudad
    estado = models.ForeignKey(Estado,on_delete=models.CASCADE)

    def __str__(self):
        """!
        Función para representar la clase de forma amigable

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        return self.nombre

class Parroquia(models.Model):
    """!
    Clase que contiene las parroquias que se encuentran un municipio

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve) / William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 14-01-2018
    @version 1.0.0
    """

    ## Nombre de la Parroquia
    nombre = models.CharField(max_length=50)

    ## Municipio en el que se encuentra ubicada la Parroquia
    municipio = models.ForeignKey(Municipio,on_delete=models.CASCADE)

    def __str__(self):
        """!
        Función para representar la clase de forma amigable

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        return self.nombre

class ConsejoComunal(models.Model):

    ## Número de rif del Consejo Comunal
    rif = models.CharField(
        max_length=10, primary_key=True
    )

    ## Nombre del Consejo Comunal
    nombre = models.CharField(max_length=500)

    ## Parroquia en el que se encuetra ubicado el Consejo Comunal
    parroquia = models.ForeignKey(Parroquia,on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = _("Consejo Comunal")
        verbose_name_plural = _("Consejos Comunales")
