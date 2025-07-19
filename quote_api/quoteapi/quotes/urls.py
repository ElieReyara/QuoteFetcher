from django.urls import path
from . import views

urlpatterns = [
    path("", views.quote, name="quote"),
    path("saveQuote/", views.saveQuote, name="saveQuote"),
    path("savedQuotes/", views.retrieveSavedQuote, name="savedQuotes")
]