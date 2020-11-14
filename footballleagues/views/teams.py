import logging
from rest_framework import generics, status
from rest_framework.response import Response
from django.db.models.functions import Now
from django.core.exceptions import ObjectDoesNotExist

from ..models.team import Team
from .helpers import *
from ..serializers import *


class TeamsAPI(generics.GenericAPIView):
    """Teams API Endpoints"""

    def get(self, request, *args, **kwargs):

        teams = Team.objects.filter(is_deleted=False)
        serialized_data = TeamsSerializer(teams, many=True).data

        rsp = {"teams": serialized_data}

        return Response(rsp)

    def post(self, request, *args, **kwargs):

        serializer = CreateTeamSerializer(data=request.data)

        if serializer.is_valid():
            league = None

            # number_of_players = 0
            # if "number_of_players" in request.data:
            #     number_of_players = request.data["number_of_players"]

            if "league" in request.data:
                league = League.objects.get(id=request.data["league"])
                if league.is_deleted:
                    return Response(
                        {"message": "League doesn't exist"},
                        status=status.HTTP_404_NOT_FOUND,
                    )

            team = Team.objects.create(
                name=request.data["name"],
                city=request.data["city"],
                coach=request.data["coach"],
                championships_won=request.data["championships_won"],
                # number_of_players=number_of_players,
                league=league,
            )

            team_serialized = TeamsSerializer(team).data
            rsp = {"team": team_serialized}

            return Response(rsp)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeamsByIdAPI(generics.GenericAPIView):
    """Teams By ID API Endpoints"""

    @validate_team
    def get(self, request, team_id, team, *args, **kwargs):

        serialized_data = TeamsSerializer(team).data

        rsp = {"team": serialized_data}

        return Response(rsp)

    @validate_team
    def put(self, request, team_id, team, *args, **kwargs):

        if not request.data:

            return Response({"message": "Body empty"}, status=status.HTTP_404_NOT_FOUND)
        else:

            serializer = UpdateTeamSerializer(team, data=request.data)

            if serializer.is_valid():
                serializer.save()

                rsp = {"team": serializer.data}
                return Response(rsp)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @validate_team
    def delete(self, request, team_id, team, *args, **kwargs):

        team.is_deleted = True
        team.save()

        rsp = {"message": "Team deleted with success"}
        return Response(rsp)
