from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("quote/", views.quote, name="quote"),
    path("random/", views.random, name="random")
]