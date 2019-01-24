from django.urls import path
from .views import(
    PersonListView, PersonCreateView
)
from django.contrib.auth.decorators import login_required

app_name = 'beneficiary'

urlpatterns = [
    path('person/list/', login_required(PersonListView.as_view()), name='person_list'),
    path('person/create/', login_required(PersonCreateView.as_view()), name='person_create'),
]
