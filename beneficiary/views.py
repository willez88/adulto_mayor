from django.shortcuts import render

# Create your views here.

class PersonListView(ListView):

    model = Person
    template_name = 'person/person_list.html'

    def get_queryset(self):

        if Person.objects.filter(communal_council_level=self.request.user.profile.communal_council_level):
            queryset = Person.objects.get(communal_council_level=self.request.user.profile.communal_council)
            return queryset
