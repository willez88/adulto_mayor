from django.urls import path, re_path
from .views import HomeView, Error403View
from .ajax import ComboUpdateView
from django.contrib.auth.decorators import login_required

app_name = 'base'

## urls de la aplicación base
urlpatterns = [
    path('', login_required(HomeView.as_view()), name='home'),
    path('error-403/', Error403View.as_view(), name = "error_403"),
]

urlpatterns += [
    re_path(r'^ajax/actualizar-combo/?$', login_required(ComboUpdateView.as_view()), name='combo_update'),
]
