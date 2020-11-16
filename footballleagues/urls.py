from django.urls import path

from .views.players import *
from .views.teams import *
from .views.leagues import *
from .views.bootstrap import *


urlpatterns = [
    path("player", PlayersAPI.as_view(), name="players"),
    path("player/<int:player_id>", PlayersByIdAPI.as_view(), name="players-details"),
    path("team", TeamsAPI.as_view(), name="teams"),
    path("team/<int:team_id>", TeamsByIdAPI.as_view(), name="teams-details"),
    path("league", LeaguesAPI.as_view(), name="leagues"),
    path("league/<int:league_id>", LeaguesByIdAPI.as_view(), name="leagues-details"),
    path("bootstrap", BootstrapAPI.as_view(), name="bootstrap"),
]
