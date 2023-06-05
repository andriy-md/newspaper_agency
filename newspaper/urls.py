from django.urls import path

from newspaper.views import (
    index,
    NewspaperListView,
    NewspaperDetailView,
    RedactorListView
)

urlpatterns = [
    path("", index, name="main-page"),
    path("newspapers/", NewspaperListView.as_view(), name="newspaper-list"),
    path("newspapers/<int:pk>/", NewspaperDetailView.as_view(), name="newspaper-detail"),
    path("redactors/", RedactorListView.as_view(), name="redactor-list"),
]

app_name = "newspaper"
