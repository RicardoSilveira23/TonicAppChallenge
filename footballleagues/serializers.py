from rest_framework import serializers

from .models.player import *
from .models.league import *
from .models.team import *


class PlayersSerializer(serializers.ModelSerializer):
    team = serializers.SerializerMethodField("get_team_name")

    class Meta:
        model = Player
        fields = ("id", "name", "age", "position", "appearances", "team")

    def get_team_name(self, obj):
        if obj.team == None:
            return None
        else:
            return obj.team.name


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
        if value is not None and value.is_deleted:
            raise serializers.ValidationError("Team doesn't exist")
        return value

    class Meta:
        model = Player
        fields = ("name", "age", "position", "appearances", "team")


class TeamsSerializer(serializers.ModelSerializer):
    league = serializers.SerializerMethodField("get_league_name")

    class Meta:
        model = Team
        fields = (
            "id",
            "name",
            "city",
            "coach",
            "championships_won",
            "number_of_players",
            "league",
        )

    def get_league_name(self, obj):
        if obj.league == None:
            return None
        else:
            return obj.league.name


class CreateTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = (
            "name",
            "city",
            "coach",
            "championships_won",
            "number_of_players",
            "league",
        )
        extra_kwargs = {
            "name": {"required": True},
            "city": {"required": True},
            "coach": {"required": True},
            "championships_won": {"required": True},
            "number_of_players": {"required": False},
        }


class UpdateTeamSerializer(serializers.ModelSerializer):
    def validate_league(self, value):
        if value.is_deleted:
            raise serializers.ValidationError("League doesn't exist")
        return value

    class Meta:
        model = Team
        fields = (
            "name",
            "city",
            "coach",
            "championships_won",
            "number_of_players",
            "league",
        )


class LeaguesSerializer(serializers.ModelSerializer):
    most_championships = serializers.SerializerMethodField(
        "get_team_with_most_championships_name"
    )
    current_champion = serializers.SerializerMethodField(
        "get_current_champion_team_name"
    )
    most_appearances = serializers.SerializerMethodField(
        "get_player_name_with_most_appearances"
    )

    class Meta:
        model = League
        fields = (
            "name",
            "country",
            "number_of_teams",
            "most_championships",
            "current_champion",
            "most_appearances",
        )

    def get_team_with_most_championships_name(self, obj):
        if obj.most_championships == None:
            return None
        else:
            return obj.most_championships.name

    def get_current_champion_team_name(self, obj):
        if obj.current_champion == None:
            return None
        else:
            return obj.current_champion.name

    def get_player_name_with_most_appearances(self, obj):
        if obj.most_appearances == None:
            return None
        else:
            return obj.most_appearances.name


class CreateLeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = (
            "name",
            "country",
            # "most_championships",
            "current_champion",
            # "most_appearances",
        )
        extra_kwargs = {
            "name": {"required": True},
            "country": {"required": True},
            # "most_championships": {"required": True},
            "current_champion": {"required": False},
            # "most_appearances": {"required": True},
        }


class UpdateLeagueSerializer(serializers.ModelSerializer):
    def validate_current_champion(self, value):
        if value.league.id != self.instance.id:
            raise serializers.ValidationError("Team doesn't belong to League")
        elif value.is_deleted:
            raise serializers.ValidationError("Team doesn't exist")
        return value

    class Meta:
        model = League
        fields = (
            "name",
            "country",
            # "most_championships",
            "current_champion",
            "number_of_teams",
            # "most_appearances",
        )
