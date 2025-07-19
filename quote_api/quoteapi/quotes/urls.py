from django.urls import path
from . import views

urlpatterns = [
    path("", views.displayQuote, name="displayQuote"),
    path("generateQuote/", views.generateQuote, name="generateQuote"),
    path("saveQuote/", views.saveQuote, name="saveQuote"),
    path("savedQuotes/", views.retrieveSavedQuote, name="retrieveSavedQuote")
]