from django.urls import path

from .views.players import *
from .views.teams import *

urlpatterns = [
    path("player", PlayersAPI.as_view(), name="players"),
    path("player/<int:player_id>", PlayersByIdAPI.as_view(), name="players-details"),
    path("team", TeamsAPI.as_view(), name="teams"),
    path("team/<int:team_id>", TeamsByIdAPI.as_view(), name="teams-details"),
]
