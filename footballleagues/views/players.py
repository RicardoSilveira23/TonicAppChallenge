import logging
from rest_framework import generics, status
from rest_framework.response import Response
from django.db.models.functions import Now
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator

from ..models.player import Player
from ..models.team import Team
from .helpers import *
from ..serializers import *


class PlayersAPI(generics.GenericAPIView):
    """Players API Endpoints"""

    serializer_class = PlayersSerializer

    def get(self, request, *args, **kwargs):
        per_page = request.GET.get("items_perpage", None)
        page_number = request.GET.get("page_number", None)

        players = Player.objects.filter(is_deleted=False)

        if per_page and page_number is not None:
            paginator = Paginator(players, per_page)
            page_content = paginator.get_page(page_number)

            serialized_data = PlayersSerializer(page_content, many=True).data
            rsp = {
                "players": serialized_data,
                "total": paginator.count,
                "page": page_content.number,
                "page_total": paginator.num_pages,
            }
            return Response(rsp)

        else:
            # Return all
            serialized_data = PlayersSerializer(players, many=True).data
            rsp = {"players": serialized_data}
            return Response(rsp)

    def post(self, request, *args, **kwargs):

        serializer = CreatePlayerSerializer(data=request.data)

        if serializer.is_valid():
            team = None

            if "team" in request.data:
                team = Team.objects.get(id=request.data["team"])
                if team.is_deleted:
                    return Response(
                        {"message": "Team doesn't exist"},
                        status=status.HTTP_404_NOT_FOUND,
                    )

            player = Player.objects.create(
                name=request.data["name"],
                age=request.data["age"],
                position=request.data["position"],
                appearances=request.data["appearances"],
                team=team,
            )

            player_serialized = PlayersSerializer(player).data
            rsp = {"player": player_serialized}

            return Response(rsp)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlayersByIdAPI(generics.GenericAPIView):
    """Players By ID API Endpoints"""

    serializer_class = PlayersSerializer

    @validate_player
    def get(self, request, player_id, player, *args, **kwargs):

        serialized_data = PlayersSerializer(player).data

        rsp = {"player": serialized_data}

        return Response(rsp)

    @validate_player
    def put(self, request, player_id, player, *args, **kwargs):

        if not request.data:

            return Response({"message": "Body empty"}, status=status.HTTP_404_NOT_FOUND)
        else:

            serializer = UpdatePlayerSerializer(player, data=request.data)

            if serializer.is_valid():
                serializer.save()

                rsp = {"player": serializer.data}
                return Response(rsp)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @validate_player
    def delete(self, request, player_id, player, *args, **kwargs):

        player.is_deleted = True
        player.save()

        rsp = {"message": "Player deleted with success"}
        return Response(rsp)
