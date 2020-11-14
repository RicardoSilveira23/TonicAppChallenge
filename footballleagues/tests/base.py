from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin

from ..models.player import Player
from ..models.team import Team
from ..models.league import League

LEAGUE_API_URL = "/api/v1/league"
LEAGUE_ID_API_URL = "/api/v1/league/"
TEAM_API_URL = "/api/v1/team"
TEAM_ID_API_URL = "/api/v1/team/"
PLAYER_API_URL = "/api/v1/player"
PLAYER_ID_API_URL = "/api/v1/player/"
