from django.db import models


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.TextField(blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True)
    updated_by = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class League(BaseModel):
    # Implicit id auto increment field created
    name = models.TextField(unique=True, blank=True, null=False)
    country = models.TextField(blank=True, null=False)
    number_of_teams = models.IntegerField(blank=True, null=False)
    most_championships = models.TextField(blank=True, null=False)
    current_champion = models.TextField(blank=True, null=False)
    most_appearances = models.TextField(blank=True, null=False)


class Team(BaseModel):
    # Implicit id auto increment field created
    name = models.TextField(unique=True, blank=True, null=False)
    city = models.TextField(blank=True, null=False)
    coach = models.TextField(blank=True, null=False)
    championships_won = models.IntegerField(blank=True, null=False, default=0)
    number_of_players = models.IntegerField(blank=True, null=False, default=0)
    league = models.ForeignKey(
        League,
        on_delete=models.DO_NOTHING,
        related_name="league",
        blank=True,
        null=True,
    )


class Player(BaseModel):
    # Implicit id auto increment field created
    name = models.TextField(blank=True, null=False)
    age = models.IntegerField(blank=True, null=False)
    position = models.TextField(blank=True, null=False)
    appearances = models.IntegerField(blank=True, null=False)
    team = models.ForeignKey(
        Team,
        on_delete=models.DO_NOTHING,
        related_name="team",
        blank=True,
        null=True,
    )
