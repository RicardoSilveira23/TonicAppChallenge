from django.db import models

# Create your models here.


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.TextField(blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.__repr__()


# name -> string
# city -> string
# championships won -> number
# coach -> string
# number of players -> number
class Team(BaseModel):
    # Implicit id auto increment field created
    name = models.TextField(unique=True, blank=True, null=False)
    city = models.TextField(blank=True, null=False)
    coach = models.TextField(blank=True, null=False)
    championships_won = models.IntegerField(blank=True, null=False, default=0)
    number_of_players = models.IntegerField(blank=True, null=False, default=0)


# name -> string
# age -> integer
# position -> string
# appearances -> integer
class Player(BaseModel):
    # Implicit id auto increment field created
    name = models.TextField(blank=True, null=False)
    age = models.IntegerField(blank=True, null=False)
    position = models.TextField(blank=True, null=False)
    appearances = models.IntegerField(blank=True, null=False)


# name -> string
# country -> string
# number of teams -> number
# current champion -> Team
# most championships -> Team
# most appearances -> Player
class League(BaseModel):
    # Implicit id auto increment field created
    name = models.TextField(unique=True, blank=True, null=False)
    country = models.TextField(blank=True, null=False)
    number_of_teams = models.IntegerField(blank=True, null=False)
    most_championships = models.ForeignKey(
        Team,
        on_delete=models.DO_NOTHING,
        related_name="most_championships_team_id",
        blank=True,
        null=False,
    )
    current_champion = models.ForeignKey(
        Team,
        on_delete=models.DO_NOTHING,
        related_name="champion_team_id",
        blank=True,
        null=False,
    )
    most_appearances = models.ForeignKey(
        Player,
        on_delete=models.DO_NOTHING,
        related_name="most_appearances_player_id",
        blank=True,
        null=False,
    )
