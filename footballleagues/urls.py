from django.urls import path

from .views.players import *

urlpatterns = [
    path("player", PlayersAPI.as_view(), name="players"),
    path("player/<int:player_id>", PlayersByIdAPI.as_view(), name="players-details"),

]