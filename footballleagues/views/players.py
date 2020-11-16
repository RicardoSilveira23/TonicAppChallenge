import logging
from rest_framework import generics, status
from rest_framework.response import Response
from django.db.models.functions import Now
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from drf_yasg.utils import swagger_auto_schema

from ..models.player import Player
from ..models.team import Team
from .helpers import *
from ..serializers import *


class PlayersAPI(generics.GenericAPIView):
    """
    Players API Endpoints
    """
    
    serializer_class = PlayersSerializer

    @swagger_auto_schema(
        responses={
            200: PlayersSerializer(many=True),
        }
    )
    def get(self, request, *args, **kwargs):
        """
        This is to get all players, allows pagination
        """
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

    @swagger_auto_schema(
        request_body=CreatePlayerSerializer,
        responses={
            200: PlayersSerializer(many=False),
            400: "Message with list of serializer errors",
        }
    )
    def post(self, request, *args, **kwargs):
        """
        Allows the creation of a new player
        """
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
    """
    Players By ID API Endpoints
    """

    serializer_class = PlayersSerializer

    @swagger_auto_schema(
        responses={
            200: PlayersSerializer(many=False),
        }
    )
    @validate_player
    def get(self, request, player_id, player, *args, **kwargs):
        """
        Gets the information of a certain player by it's ID
        """
        serialized_data = PlayersSerializer(player).data

        rsp = {"player": serialized_data}

        return Response(rsp)

    @swagger_auto_schema(
        request_body=UpdatePlayerSerializer,
        responses={
            200: UpdatePlayerSerializer(many=False),
            400: "Message with list of serializer errors",
            404: "Body empty",
        }
    )
    @validate_player
    def put(self, request, player_id, player, *args, **kwargs):
        """
        Allows the update of a certain player details based on ID
        """
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

    @swagger_auto_schema(responses={200: "Player deleted with success"})
    @validate_player
    def delete(self, request, player_id, player, *args, **kwargs):
        """
        Allows to delete a player by id
        """
        player.is_deleted = True
        player.save()

        rsp = {"message": "Player deleted with success"}
        return Response(rsp)
