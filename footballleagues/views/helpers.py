from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

from ..models import *


def validate_player(func):
    def modified(self, request, player_id, *args, **kwargs):

        try:
            player = Player.objects.get(id=player_id)
        except ObjectDoesNotExist:
            return Response(
                {"message": "Player ID is not valid"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if player.is_deleted:
            return Response(
                {"message": "Player doesn't exist"}, status=status.HTTP_404_NOT_FOUND
            )
        else:
            return func(self, request, player_id, player)

    return modified


def validate_team(func):
    def modified(self, request, team_id, *args, **kwargs):

        try:
            team = Team.objects.get(id=team_id)
        except ObjectDoesNotExist:
            return Response(
                {"message": "Team ID is not valid"}, status=status.HTTP_400_BAD_REQUEST
            )

        if team.is_deleted:
            return Response(
                {"message": "Team doesn't exist"}, status=status.HTTP_404_NOT_FOUND
            )
        else:
            return func(self, request, team_id, team)

    return modified
