from django.urls import path

from newspaper.views import index


urlpatterns = [
    path("", index, name="main-page"),
]

app_name = "newspaper"
