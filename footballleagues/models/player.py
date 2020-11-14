from .base import *
from .team import *


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

    # class Meta:
    #     indexes = [models.Index(fields=["name"], name="player_name_idx")]


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
    if instance.team is not None:
        if created:
            instance.team.number_of_players += 1
            instance.team.save()
        elif instance.is_deleted:
            instance.team.number_of_players -= 1
            instance.team.save()
