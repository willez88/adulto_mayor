from django.utils.translation import ugettext_lazy as _

## Nacionalidades (ABREVIADO)
NACIONALIDAD = (
    ('V', 'V'), ('E', 'E')
)

NIVEL = (
    (1, 'Nivel Estadal'),
    (2, 'Nivel Municipal'),
    (3, 'Nivel Parroquial'),
)

## Mensaje de error para peticiones AJAX
MSG_NOT_AJAX = _("No se puede procesar la petición. "
                 "Verifique que posea las opciones javascript habilitadas e intente nuevamente.")
