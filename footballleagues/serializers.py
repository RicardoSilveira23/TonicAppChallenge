from rest_framework import serializers

from .models import *


class PlayersSerializer(serializers.ModelSerializer):
    team = serializers.ReadOnlyField(source="team.name")

    class Meta:
        model = Player
        fields = ("id", "name", "age", "position", "appearances", "team")


class CreatePlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ("name", "age", "position", "appearances", "team")
        extra_kwargs = {
            "name": {"required": True},
            "age": {"required": True},
            "position": {"required": True},
            "appearances": {"required": True},
        }


class UpdatePlayerSerializer(serializers.ModelSerializer):
    def validate_team(self, value):
        if value.is_deleted:
            raise serializers.ValidationError("Team doesn't exist")
        return value

    class Meta:
        model = Player
        fields = ("name", "age", "position", "appearances", "team")


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
        fields = (
            "name",
            "city",
            "coach",
            "championships_won",
            "number_of_players",
        )


class LeaguesSerializer(serializers.ModelSerializer):
    most_championships = serializers.ReadOnlyField(source="most_championships.name")
    current_champion = serializers.ReadOnlyField(source="current_champion.name")
    most_appearances = serializers.ReadOnlyField(source="most_appearances.name")

    class Meta:
        model = League
        fields = (
            "name",
            "country",
            "most_championships",
            "current_champion",
            "most_appearances",
        )


class CreateLeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = (
            "name",
            "country",
            "most_championships",
            "current_champion",
            "most_appearances",
        )
        extra_kwargs = {
            "name": {"required": True},
            "country": {"required": True},
            "most_championships": {"required": True},
            "current_champion": {"required": True},
            "most_appearances": {"required": True},
        }
