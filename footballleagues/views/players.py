import logging
from rest_framework import generics, status
from rest_framework.response import Response
from django.db.models.functions import Now
from django.core.exceptions import ObjectDoesNotExist

from ..models import Player
from .helpers import *
from ..serializers import *


class PlayersAPI(generics.GenericAPIView):
    """Players API Endpoints"""

    def get(self, request, *args, **kwargs):

        players = Player.objects.filter(is_deleted=False)
        serialized_data = PlayersSerializer(players, many=True).data

        rsp = {"players": serialized_data}

        return Response(rsp)

    def post(self, request, *args, **kwargs):

        serializer = CreatePlayerSerializer(data=request.data)

        if serializer.is_valid():

            player = Player.objects.create(
                name=request.data["name"],
                age=request.data["age"],
                position=request.data["position"],
                appearances=request.data["appearances"],
            )

            player_serialized = PlayersSerializer(player).data
            rsp = {"player": player_serialized}

            return Response(rsp)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlayersByIdAPI(generics.GenericAPIView):
    """Players By ID API Endpoints"""

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
