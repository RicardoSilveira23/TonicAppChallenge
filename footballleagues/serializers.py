from rest_framework import serializers
from .models import *

class PlayersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Player
        fields = (
            "id",
            "name",
            "age",
            "position",
            "appearances"
        )

class CreatePlayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Player
        fields = ("name", "age", "position", "appearances")
        extra_kwargs = {
            "name" : {"required" : True},
            "age" : {"required" : True},
            "position" : {"required" : True},
            "appearances" : {"required": True}
        }

class UpdatePlayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Player
        fields = ("name", "age", "position", "appearances")

        