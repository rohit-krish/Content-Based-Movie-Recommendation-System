from django.urls import path
from . import views

urlpatterns = [
    path("", views.home),
    path("detail_data", views.detail_data),
]

