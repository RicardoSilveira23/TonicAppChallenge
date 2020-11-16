import logging
import random
from rest_framework import generics, status
from rest_framework.response import Response
from django.db import transaction


from ..models.league import League
from ..models.player import Player
from ..models.team import Team


class BootstrapAPI(generics.GenericAPIView):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """
        Allows initialization of data to the DB
        """
        num_of_leagues = request.data.get("num_leagues", 40)
        num_of_teams = request.data.get("num_of_teams", 18)
        num_of_players = request.data.get("num_of_players", 27)
        positions = ["Goalkeeper", "Defender", "Midfielder", "Forward"]

        for x in range(num_of_leagues):
            league = League.objects.create(
                name="New Name " + str(x),
                country="Country " + str(random.randint(0, num_of_leagues)),
            )

            for y in range(num_of_teams):
                team = Team.objects.create(
                    name="Team " + str(x) + "-" + str(y),
                    city="City " + str(random.randint(0, num_of_teams)),
                    coach="Coach " + str(x) + str(y),
                    championships_won=random.randint(0, 100),
                    league=league,
                )

                for z in range(num_of_players):
                    Player.objects.create(
                        name="Player " + str(z),
                        age=random.randint(20, 45),
                        position=random.choice(positions),
                        appearances=random.randint(10, 450),
                        team=team,
                    )

            league.current_champion = team
            league.save()

        return Response()
