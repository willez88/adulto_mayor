# Adulto Mayor

Este sistema recopila los datos de los adultos mayores.

# Pasos para crear el entorno de desarrollo

Cuando somos un usuario normal del sistema, en el terminal se mostrará el siguiente símbolo: ~$

Cuando accedemos al usuario root del sistema, en el terminal se mostrará el siguiente símbolo: ~#

Probado en Debian y Ubuntu en sus últimas versiones estables. Instalar los siguientes programas

    ~# apt install curl git graphviz graphviz-dev phppgadmin postgresql python3-dev virtualenv

Para instalar npm hacer lo siguiente

    ~# curl -sL https://deb.nodesource.com/setup_13.x | bash -

    ~# apt install -y nodejs

    // Con el comando anterior se debe instalar npm, en caso contrario
    ~# apt install -y npm

Crear las siguientes carpetas

    ~$ mkdir Programación

Desde el terminal, moverse a la carpeta Programación y ejecutar

    ~$ cd Programación/

    ~$ mkdir python

Entrar a la carpeta python y hacer lo siguiente

    ~$ cd python/

    ~$ mkdir entornos_virtuales proyectos_django

Entrar a entornos_virtuales

    ~$ cd entornos_virtuales/

    ~$ mkdir django

Desde el terminal, moverse a la carpeta django y ejecutar

    ~$ cd django/

    ~$ virtualenv -p python3 adulto_mayor

Para activar el entorno

    ~$ source adulto_mayor/bin/activate

Nos movemos a la carpeta proyectos_django, descargamos el sistema y entramos a la carpeta con los siguientes comandos

    (adulto_mayor) ~$ cd ../../proyectos_django/

    (adulto_mayor) ~$ git clone https://github.com/willez88/adulto_mayor.git

    (adulto_mayor) ~$ cd adulto_mayor/

    (adulto_mayor) ~$ cp adulto_mayor/settings.default.py adulto_mayor/settings.py

Tendremos las carpetas estructuradas de la siguiente manera

    // Entorno virtual
    Programación/python/entornos_virtuales/django/adulto_mayor

    // Servidor de desarrollo
    Programación/python/proyectos_django/adulto_mayor

Instalar las dependencias de css y js: moverse a la carpeta static y ejecutar

    (adulto_mayor) ~$ cd static/

    // Usa el archivo package.json para instalar lo que ya se configuró allí
    (adulto_mayor) ~$ npm install

    // Terminado el proceso volver a la carpeta raíz del proyecto
    (adulto_mayor) ~$ cd ../

Crear la base de datos para __adulto_mayor__ usando PostgresSQL

    // Acceso al usuario postgres
    ~# su postgres

    // Acceso a la interfaz de comandos de PostgreSQL
    postgres@xxx:$ psql

    // Creación del usuario de a base de datos
    postgres=# CREATE USER admin WITH LOGIN ENCRYPTED PASSWORD '123' CREATEDB;
    postgres=# \q

    // Desautenticar el usuario PostgreSQL y regresar al usuario root
    postgres@xxx:$ exit

    // Salir del usuario root
    ~# exit

Puedes crear la base de datos usando la interfaz gráfica de phppgadmin o desde cualquier otra que desee

    // Nombre de la base de datos: adulto_mayor

Instalamos los requemientos que el sistema necesita en el entorno virtual

    (adulto_mayor) ~$ pip install -r requirements/dev.txt

Hacer las migraciones

    (adulto_mayor) ~$ python manage.py makemigrations base user beneficiary

    (adulto_mayor) ~$ python manage.py migrate

    (adulto_mayor) ~$ python manage.py loaddata 1_country.json 2_state.json 3_municipality.json 4_city.json 5_parish.json 6_communal_council.json base.json

Crear usuario administrador

    (adulto_mayor) ~$ python manage.py createsuperuser

Correr el servidor de django

    (adulto_mayor) ~$ python manage.py runserver

Poner en el navegador la url que sale en el terminal para entrar el sistema

Llegado hasta aquí el sistema ya debe estar funcionando

Para salir del entorno virtual se puede ejecutar desde cualquier lugar del terminal: deactivate
