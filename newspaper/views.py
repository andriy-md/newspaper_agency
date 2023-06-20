from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic

from newspaper.forms import NewspaperForm, NewspaperSearchForm, RedactorForm
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
    paginate_by = 7

    def get_queryset(self):
        queryset = Newspaper.objects.all().prefetch_related("publishers")

        title_search = self.request.GET.get("search_title")
        if title_search:
            queryset = queryset.filter(title__icontains=title_search)

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = NewspaperSearchForm()
        return context


class NewspaperDetailView(generic.DetailView):
    model = Newspaper


class NewspaperCreateView(LoginRequiredMixin, generic.CreateView):
    model = Newspaper
    form_class = NewspaperForm

    def get_success_url(self):
        return reverse("newspaper:newspaper-detail", kwargs={"pk": self.object.pk})


class NewspaperUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Newspaper
    form_class = NewspaperForm

    def get_success_url(self):
        return reverse("newspaper:newspaper-detail", kwargs={"pk": self.object.pk})


class NewspaperDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Newspaper
    success_url = reverse_lazy("newspaper:newspaper-list")


class RedactorListView(generic.ListView):
    model = get_user_model()
    paginate_by = 10


class RedactorDetailView(generic.DetailView):
    model = get_user_model()


class RedactorCreateView(generic.CreateView):
    model = get_user_model()
    form_class = RedactorForm

    def get_success_url(self):
        return reverse("newspaper:redactor-detail", kwargs={"pk": self.object.pk})


class RedactorUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = get_user_model()
    form_class = RedactorForm

    def get_success_url(self):
        return reverse("newspaper:redactor-detail", kwargs={"pk": self.object.pk})


class RedactorDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = get_user_model()
    success_url = reverse_lazy("")
