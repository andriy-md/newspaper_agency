from django.urls import path

from newspaper.views import (
    index,
    NewspaperListView,
    NewspaperDetailView,
    NewspaperCreateView,
    NewspaperUpdateView,
    RedactorListView,
    RedactorDetailView,
)

urlpatterns = [
    path("", index, name="main-page"),
    path("newspapers/", NewspaperListView.as_view(), name="newspaper-list"),
    path("newspapers/create/", NewspaperCreateView.as_view(), name="newspaper-create"),
    path("newspapers/<int:pk>/", NewspaperDetailView.as_view(), name="newspaper-detail"),
    path("newspapers/<int:pk>/update/", NewspaperUpdateView.as_view(), name="newspaper-update"),
    path("redactors/", RedactorListView.as_view(), name="redactor-list"),
    path("redactors/<int:pk>/", RedactorDetailView.as_view(), name="redactor-detail"),
]

app_name = "newspaper"
