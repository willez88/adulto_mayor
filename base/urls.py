from django.urls import path
from .views import HomeView, Error403View
from django.contrib.auth.decorators import login_required

app_name = 'base'

## urls de la aplicación base
urlpatterns = [
    path('', login_required(HomeView.as_view()), name='home'),
    path('error-403/', Error403View.as_view(), name = "error_403"),
]
