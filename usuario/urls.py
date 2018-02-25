from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .views import MunicipalList, MunicipalCreate, EstadalUpdate, ParroquialList, ParroquialCreate, MunicipalUpdate, ParroquialUpdate, ComunalList, ComunalCreate, ComunalUpdate

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('reset/password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html',
        email_template_name='password_reset_email.html'),
        name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
        name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'),

    path('cambiar-clave/', login_required(auth_views.PasswordChangeView.as_view(template_name='password_change_form.html')), name='password_change'),
    path('cambiar-clave-hecho/', login_required(auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html')), name='password_change_done'),

    path('estadal/actualizar/<int:pk>/', login_required(EstadalUpdate.as_view()), name='estadal_actualizar'),
    path('municipal/', login_required(MunicipalList.as_view()), name='municipal_listar'),
    path('municipal/registrar/', login_required(MunicipalCreate.as_view()), name='municipal_registrar'),

    path('municipal/actualizar/<int:pk>/', login_required(MunicipalUpdate.as_view()), name='municipal_actualizar'),
    path('parroquial/', login_required(ParroquialList.as_view()), name='parroquial_listar'),
    path('parroquial/registrar/', login_required(ParroquialCreate.as_view()), name='parroquial_registrar'),

    path('parroquial/actualizar/<int:pk>/', login_required(ParroquialUpdate.as_view()), name='parroquial_actualizar'),
    path('comunal/', login_required(ComunalList.as_view()), name='comunal_listar'),
    path('comunal/registrar/', login_required(ComunalCreate.as_view()), name='comunal_registrar'),

    path('comunal/actualizar/<int:pk>/', login_required(ComunalUpdate.as_view()), name='comunal_actualizar'),
]
