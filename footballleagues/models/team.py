from .base import *
from .league import *


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

    # class Meta:
    #     indexes = [
    #         models.Index(
    #             fields=[
    #                 "name",
    #                 "city",
    #                 "coach",
    #                 "championships_won",
    #                 "number_of_players",
    #             ],
    #             name="team_idx",
    #         )
    #     ]


# PRE_SAVE - if league changes, change count
@receiver(pre_save, sender=Team)
def update_league_team(sender, instance, **kwargs):
    try:
        team = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        pass
        # Object is new, update will happen in post_save
    else:
        pass
        # # Validate if team changed league
        # if instance.league == None:
        #     team.league.number_of_teams -= 1
        #     team.league.save()
        # elif not team.league == instance.league:
        #     team.league.number_of_teams -= 1
        #     team.league.save()
        #     instance.league.number_of_teams += 1
        #     instance.league.save()


# POST_SAVE - check if team is being deleted or if new add to league team count
@receiver(post_save, sender=Team)
def new_or_deleted_league_team(sender, instance, created, **kwargs):
    if instance.league is not None:
        if created:
            instance.league.number_of_teams += 1
            instance.league.save()
        elif instance.is_deleted:
            instance.league.number_of_teams -= 1
            instance.league.save()
