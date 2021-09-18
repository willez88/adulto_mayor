from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
from django.urls import path, reverse_lazy

from .views import (
    CommunalCouncilLevelCreateView, CommunalCouncilLevelListView,
    CommunalCouncilLevelUpdateView, MunicipalLevelCreateView,
    MunicipalLevelListView, MunicipalLevelUpdateView, NationalLevelUpdateView,
    ParishLevelCreateView, ParishLevelListView, ParishLevelUpdateView,
    StateLevelCreateView, StateLevelListView, StateLevelUpdateView,
)


app_name = 'user'

urlpatterns = [
    path(
        'login/', views.LoginView.as_view(template_name='user/login.html'),
        name='login'
    ),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path(
        'reset/password_reset/',
        views.PasswordResetView.as_view(
            template_name='user/password_reset_form.html',
            email_template_name='user/password_reset_email.html',
            success_url=reverse_lazy('user:password_reset_done')
        ),
        name='password_reset'
    ),
    path(
        'password_reset_done/',
        views.PasswordResetDoneView.as_view(
            template_name='user/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        views.PasswordResetConfirmView.as_view(
            template_name='user/password_reset_confirm.html',
            success_url=reverse_lazy('user:password_reset_complete')
        ),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        views.PasswordResetCompleteView.as_view(
            template_name='user/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),

    path(
        'password-change/',
        login_required(
            views.PasswordChangeView.as_view(
                template_name='user/password_change_form.html'
            )
        ),
        name='password_change'
    ),
    path(
        'password-change-done/',
        login_required(
            views.PasswordChangeDoneView.as_view(
                template_name='user/password_change_done.html'
            )
        ),
        name='password_change_done'
    ),

    path(
        'national-level/update/<int:pk>/',
        login_required(NationalLevelUpdateView.as_view()),
        name='national_level_update'
    ),
    path(
        'state-level/',
        login_required(StateLevelListView.as_view()),
        name='state_level_list'
    ),
    path(
        'state-level/create/',
        login_required(StateLevelCreateView.as_view()),
        name='state_level_create'
    ),

    path(
        'state-level/update/<int:pk>/',
        login_required(StateLevelUpdateView.as_view()),
        name='state_level_update'
    ),
    path(
        'municipality-level/',
        login_required(MunicipalLevelListView.as_view()),
        name='municipal_level_list'
    ),
    path(
        'municipality-level/create/',
        login_required(MunicipalLevelCreateView.as_view()),
        name='municipal_level_create'
    ),

    path(
        'municipality-level/update/<int:pk>/',
        login_required(MunicipalLevelUpdateView.as_view()),
        name='municipal_level_update'
    ),
    path(
        'parish-level/', login_required(ParishLevelListView.as_view()),
        name='parish_level_list'
    ),
    path(
        'parish-level/create/',
        login_required(ParishLevelCreateView.as_view()),
        name='parish_level_create'
    ),

    path(
        'parish-level/update/<int:pk>/',
        login_required(ParishLevelUpdateView.as_view()),
        name='parish_level_update'
    ),
    path(
        'communal-council-level/',
        login_required(CommunalCouncilLevelListView.as_view()),
        name='communal_council_level_list'
    ),
    path(
        'communal-council-level/create/',
        login_required(CommunalCouncilLevelCreateView.as_view()),
        name='communal_council_level_create'
    ),

    path(
        'communal-council-level/update/<int:pk>/',
        login_required(CommunalCouncilLevelUpdateView.as_view()),
        name='communal_council_level_update'
    ),
]
