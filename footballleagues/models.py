from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save


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


# PRE_SAVE - if team changes, change count
@receiver(pre_save, sender=Player)
def update_team_player(sender, instance, **kwargs):
    try:
        player = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        pass
        # Object is new, update will happen in post_save
    else:
        # Validate if player changed team
        if instance.team == None:
            player.team.number_of_players -= 1
            player.team.save()
        elif not player.team == instance.team:
            player.team.number_of_players -= 1
            player.team.save()
            instance.team.number_of_players += 1
            instance.team.save()


# POST_SAVE - check if player is being deleted or if new add to team player count
@receiver(post_save, sender=Player)
def new_or_deleted_team_player(sender, instance, created, **kwargs):
    if created:
        instance.team.number_of_players += 1
        instance.team.save()
    elif instance.is_deleted:
        instance.team.number_of_players -= 1
        instance.team.save()
