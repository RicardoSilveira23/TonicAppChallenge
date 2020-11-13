from rest_framework import serializers
from .models import *


class PlayersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ("id", "name", "age", "position", "appearances")


class CreatePlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ("name", "age", "position", "appearances")
        extra_kwargs = {
            "name": {"required": True},
            "age": {"required": True},
            "position": {"required": True},
            "appearances": {"required": True},
        }


class UpdatePlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ("name", "age", "position", "appearances")


class TeamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = (
            "id",
            "name",
            "city",
            "coach",
            "championships_won",
            "number_of_players",
        )


class CreateTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ("name", "city", "coach", "championships_won", "number_of_players")
        extra_kwargs = {
            "name": {"required": True},
            "city": {"required": True},
            "coach": {"required": True},
            "championships_won": {"required": True},
            "number_of_players": {"required": True},
        }


class UpdateTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = fields = (
            "name",
            "city",
            "coach",
            "championships_won",
            "number_of_players",
        )
