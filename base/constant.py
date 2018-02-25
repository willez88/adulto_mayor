from django.utils.translation import ugettext_lazy as _

## Nombre del Sitio
APP_NAME = "Adulto Mayor"

## Asunto del mensaje de bienvenida
EMAIL_SUBJECT_REGISTRO = "Bienvenido a %s" % APP_NAME

## Nacionalidades (ABREVIADO)
NACIONALIDAD = (
    ('V', 'V'), ('E', 'E')
)

## Establece los diferentes niveles de un usuario
NIVEL = (
    (0, 'administrador'),
    (1, 'Nivel Estadal'),
    (2, 'Nivel Municipal'),
    (3, 'Nivel Parroquial'),
    (4, 'Nivel Comunal'),
)

## Mensaje de error para peticiones AJAX
MSG_NOT_AJAX = _("No se puede procesar la petición. "
                 "Verifique que posea las opciones javascript habilitadas e intente nuevamente.")
