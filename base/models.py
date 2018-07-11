from django.db import models
from django.utils.translation import ugettext_lazy as _

class Country(models.Model):
    """!
    Clase que contiene los paises

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 14-01-2018
    @version 1.0.0
    """

    ## Nombre del pais
    name = models.CharField(max_length=80)

    def __str__(self):
        """!
        Función para representar la clase de forma amigable

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        return self.name

class State(models.Model):
    """!
    Clase que contiene los estados que se encuentran en un país

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 14-01-2018
    @version 1.0.0
    """

    ## Nombre del Estado
    name = models.CharField(max_length=50)

    ## Pais en donde esta ubicado el Estado
    country = models.ForeignKey(Country,on_delete=models.CASCADE)

    def __str__(self):
        """!
        Función para representar la clase de forma amigable

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        return self.name

class Municipality(models.Model):
    """!
    Clase que contiene los municipios que se encuentran en un estado

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 14-01-2018
    @version 1.0.0
    """

    ## Nombre del Municipio
    name = models.CharField(max_length=50)

    ## Estado en donde se encuentra el Municipio
    state = models.ForeignKey(State,on_delete=models.CASCADE)

    def __str__(self):
        """!
        Función para representar la clase de forma amigable

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        return self.name

class City(models.Model):
    """!
    Clase que contiene las ciudades que se encuentran en un estado

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 14-01-2018
    @version 1.0.0
    """

    ## Nombre de la Ciudad
    name = models.CharField(max_length=50)

    ## Estado en donde se encuentra ubicada la Ciudad
    state = models.ForeignKey(State,on_delete=models.CASCADE)

    def __str__(self):
        """!
        Función para representar la clase de forma amigable

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        return self.name

class Parish(models.Model):
    """!
    Clase que contiene las parroquias que se encuentran un municipio

    @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
    @author William Páez (wpaez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 14-01-2018
    @version 1.0.0
    """

    ## Nombre de la Parroquia
    name = models.CharField(max_length=50)

    ## Municipio en el que se encuentra ubicada la Parroquia
    municipality = models.ForeignKey(Municipality,on_delete=models.CASCADE)

    def __str__(self):
        """!
        Función para representar la clase de forma amigable

        @author William Páez (wpaez at cenditel.gob.ve)
        @copyright <a href='http://www.gnu.org/licenses/gpl-3.0.html'>GNU Public License versión 3 (GPLv3)</a>
        @date 14-01-2018
        @version 1.0.0
        """

        return self.name

class CommunalCouncil(models.Model):

    ## Número de rif del Consejo Comunal
    rif = models.CharField(
        max_length=10, primary_key=True
    )

    ## Nombre del Consejo Comunal
    name = models.CharField(max_length=500, verbose_name='Nombre')

    ## Parroquia en el que se encuetra ubicado el Consejo Comunal
    parish = models.ForeignKey(Parish,on_delete=models.CASCADE, verbose_name='Parroquia')

    def __str__(self):
        return self.rif + ' | ' + self.name

    class Meta:
        verbose_name = _("Consejo Comunal")
        verbose_name_plural = _("Consejos Comunales")
