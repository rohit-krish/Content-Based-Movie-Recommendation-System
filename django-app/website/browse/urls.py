from django.urls import path
from . import views

urlpatterns = [
    path("", views.home),
    path("html_data", views.html_data),
]
