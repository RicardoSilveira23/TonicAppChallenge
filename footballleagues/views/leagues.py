import logging
from rest_framework import generics, status
from rest_framework.response import Response
from django.db.models import Q, Count
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator


from ..models.league import League
from .helpers import *
from ..serializers import *


class LeaguesAPI(generics.GenericAPIView):
    """Leagues API Endpoints"""

    def get(self, request, *args, **kwargs):
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
                Player.objects.filter(Q(is_deleted=False) & Q(name__icontains=name))
                .values_list("team_id", flat=True)
                .distinct()
            )
            leagues = leagues.filter(teams__id__in=teams_ids)

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

    def post(self, request, *args, **kwargs):

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

    @validate_league
    def get(self, request, league_id, league, *args, **kwargs):

        serialized_data = LeaguesSerializer(league).data

        rsp = {"league": serialized_data}

        return Response(rsp)

    @validate_league
    def put(self, request, league_id, league, *args, **kwargs):

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

    @validate_league
    def delete(self, request, league_id, league, *args, **kwargs):

        league.is_deleted = True
        league.save()

        rsp = {"message": "League deleted with success"}
        return Response(rsp)
