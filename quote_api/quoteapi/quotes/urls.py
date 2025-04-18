from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("quotes/quote", views.quote, name="quote"),
    path("/random", views.random, name="random")
]