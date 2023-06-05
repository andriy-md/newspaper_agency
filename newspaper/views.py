from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views import generic

from newspaper.models import Newspaper, Topic


def index(request):
    context = {
        "newspapers": Newspaper.objects.all(),
        "topics": Topic.objects.all(),
        "redactors": get_user_model().objects.all()
    }

    return render(request, "newspaper/index.html", context)


class NewspaperListView(generic.ListView):
    model = Newspaper


class NewspaperDetailView(generic.DetailView):
    model = Newspaper


class RedactorListView(generic.ListView):
    model = get_user_model()

