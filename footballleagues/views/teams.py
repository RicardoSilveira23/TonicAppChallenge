import logging
from rest_framework import generics, status
from rest_framework.response import Response
from django.db.models.functions import Now
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator

from ..models.team import Team
from .helpers import *
from ..serializers import *


class TeamsAPI(generics.GenericAPIView):
    """Teams API Endpoints"""

    def get(self, request, *args, **kwargs):
        # filter by name, city, n champs, coach name, number of players
        # allow pagination
        per_page = request.GET.get("items_perpage", None)
        page_number = request.GET.get("page_number", None)
        name = request.GET.get("name", None)
        city = request.GET.get("city", None)
        num_champs = request.GET.get("num_champs", None)
        coach = request.GET.get("coach", None)
        number_of_players = request.GET.get("number_of_players", None)

        teams = Team.objects.filter(is_deleted=False)

        teams = teams_filtering(teams,name,city,num_champs, coach, number_of_players)

        if per_page and page_number is not None:
            paginator = Paginator(teams.order_by("-created_date"), per_page)
            page_content = paginator.get_page(page_number)

            serialized_data = TeamsSerializer(page_content, many=True).data
            rsp = {
                "teams": serialized_data,
                "total": paginator.count,
                "page": page_content.number,
                "page_total": paginator.num_pages,
            }
            return Response(rsp)
        else:
            # Return all
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

def teams_filtering(teams, name,city,num_champs, coach, number_of_players):

    if name is not None:
        # filter by name
        teams = Team.objects.filter(name__icontains=name)
    if city is not None:
        # filter by city
        teams = Team.objects.filter(city__icontains=city)
    if num_champs is not None:
        # filter by num_champs
        teams = Team.objects.filter(championships_won=num_champs)
    if coach is not None:
        # filter by coach
        teams = Team.objects.filter(coach__icontains=coach)
    if number_of_players is not None:
        # filter by number_of_players
        teams = Team.objects.filter(number_of_players=number_of_players)

    return teams
        
       

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
