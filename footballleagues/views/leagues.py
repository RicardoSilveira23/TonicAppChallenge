import logging
from rest_framework import generics, status
from rest_framework.response import Response
from django.db.models import Q, Count
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from drf_yasg.utils import swagger_auto_schema


from ..models.league import League
from .helpers import *
from ..serializers import *


class LeaguesAPI(generics.GenericAPIView):
    """
    Leagues API Endpoints
    """

    serializer_class = LeaguesSerializer

    @swagger_auto_schema(
        responses={
            200: LeaguesSerializer(many=True),
        }
    )
    def get(self, request, *args, **kwargs):
        """
        This is to get all leagues, allows pagination and filtering by player name
        """
        # filter by name of player
        # allow pagination
        per_page = request.GET.get("items_perpage", None)
        page_number = request.GET.get("page_number", None)
        name = request.GET.get("name", None)

        leagues = League.objects.filter(is_deleted=False)

        if name is not None:
            # filter by player name
            # filter by players, that team not null, teams distinct
            teams_ids = (
                Player.objects.filter(Q(is_deleted=False) & Q(name__search=name))
                .values_list("team_id", flat=True)
                .distinct()
            )
            leagues = leagues.filter(teams__id__in=teams_ids).distinct()

        if per_page and page_number is not None:
            paginator = Paginator(leagues.order_by("-created_date"), per_page)
            page_content = paginator.get_page(page_number)

            serialized_data = LeaguesSerializer(page_content, many=True).data
            rsp = {
                "leagues": serialized_data,
                "total": paginator.count,
                "page": page_content.number,
                "page_total": paginator.num_pages,
            }
            return Response(rsp)
        else:
            # Return all
            serialized_data = LeaguesSerializer(leagues, many=True).data
            rsp = {"leagues": serialized_data}
            return Response(rsp)

    @swagger_auto_schema(
        request_body=CreateLeagueSerializer,
        responses={
            200: LeaguesSerializer(many=False),
            400: "Message with list of serializer errors",
            404: "Team doesn't exist",
        },
    )
    def post(self, request, *args, **kwargs):
        """
        Allows the creation of a new league
        """
        serializer = CreateLeagueSerializer(data=request.data)

        if serializer.is_valid():
            team_champion = None

            if "current_champion" in request.data:
                team_champion = Team.objects.get(id=request.data["current_champion"])
                if team_champion.is_deleted:
                    return Response(
                        {"message": "Team doesn't exist"},
                        status=status.HTTP_404_NOT_FOUND,
                    )

            league = League.objects.create(
                name=request.data["name"],
                country=request.data["country"],
                # number_of_teams=request.data["number_of_teams"],
                current_champion=team_champion,
                # most_championships=request.data["most_championships"],
                # most_appearances=request.data["most_appearances"],
            )

            league_serialized = LeaguesSerializer(league).data
            rsp = {"league": league_serialized}

            return Response(rsp)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LeaguesByIdAPI(generics.GenericAPIView):
    """Leagues By ID API Endpoints"""

    serializer_class = LeaguesSerializer

    @swagger_auto_schema(
        responses={
            200: LeaguesSerializer(many=False),
        }
    )
    @validate_league
    def get(self, request, league_id, league, *args, **kwargs):
        """
        Gets the information of a certain league by it's ID
        """
        serialized_data = LeaguesSerializer(league).data

        rsp = {"league": serialized_data}

        return Response(rsp)

    @swagger_auto_schema(
        request_body=UpdateLeagueSerializer,
        responses={
            200: UpdateLeagueSerializer(many=False),
            400: "Message with list of serializer errors",
            404: "Body empty",
        },
    )
    @validate_league
    def put(self, request, league_id, league, *args, **kwargs):
        """
        Allows the update of a certain league details based on ID
        """
        if not request.data:

            return Response({"message": "Body empty"}, status=status.HTTP_404_NOT_FOUND)
        else:

            serializer = UpdateLeagueSerializer(league, data=request.data)

            if serializer.is_valid():
                serializer.save()

                rsp = {"league": serializer.data}
                return Response(rsp)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={200: "League deleted with success"})
    @validate_league
    def delete(self, request, league_id, league, *args, **kwargs):
        """
        Allows to delete a league by id
        """
        league.is_deleted = True
        league.save()

        rsp = {"message": "League deleted with success"}
        return Response(rsp)
