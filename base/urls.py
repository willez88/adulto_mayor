from django.urls import path
from .views import InicioView, Error403View
from django.contrib.auth.decorators import login_required

## urls de la aplicación base
urlpatterns = [
    path('', login_required(InicioView.as_view()), name='inicio'),
    path('error-403/', Error403View.as_view(), name = "error_403"),
]
