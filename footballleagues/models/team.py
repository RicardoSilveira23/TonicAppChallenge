from .base import *
from .league import *


class Team(BaseModel):
    # Implicit id auto increment field created
    name = models.TextField(unique=True, blank=True, null=False)
    city = models.TextField(db_index=True, blank=True, null=False)
    coach = models.TextField(db_index=True, blank=True, null=False)
    championships_won = models.IntegerField(
        blank=True, null=False, default=0, db_index=True
    )
    number_of_players = models.IntegerField(
        blank=True, null=False, default=0, db_index=True
    )
    league = models.ForeignKey(
        League,
        on_delete=models.DO_NOTHING,
        related_name="teams",
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
        new_league = instance.league
        current_league = team.league

        # No league -> new league
        if current_league == None and new_league != None:
            new_league.number_of_teams += 1
            new_league.save()
            compare_most_championships(new_league, instance)

        # League -> no League
        elif current_league != None and new_league == None:
            current_league.number_of_teams -= 1
            current_league.save()
            query_most_championships(current_league, instance)

        # Changed League
        elif not current_league == new_league:
            current_league.number_of_teams -= 1
            current_league.save()
            query_most_championships(current_league, instance)

            new_league.number_of_teams += 1
            new_league.save()
            compare_most_championships(new_league, instance)

        # Changed number of championships but remained in same league
        elif (
            current_league == new_league
            and team.championships_won != instance.championships_won
        ):
            compare_most_championships(current_league, instance)


# POST_SAVE - check if team is being deleted or if new add to league team count
@receiver(post_save, sender=Team)
def new_or_deleted_league_team(sender, instance, created, **kwargs):
    league = instance.league
    if league is not None:
        if created:
            if not instance.is_deleted:
                league.number_of_teams += 1
                league.save()
                compare_most_championships(league, instance)

        elif instance.is_deleted:
            league.number_of_teams -= 1
            league.save()
            query_most_championships(league, instance)


def compare_most_championships(league, team):
    # if team has a league its required to calculate most_championships field
    if league.most_championships is not None:
        if league.most_championships.championships_won < team.championships_won:
            league.most_championships = team
            league.save()
    else:
        league.most_championships = team
        league.save()


def query_most_championships(league, team):
    if league.most_championships == team:
        # query most_championships
        team_with_most = (
            Team.objects.filter(is_deleted=False, league=league)
            .exclude(id=team.id)
            .order_by("-championships_won")
            .first()
        )
        league.most_championships = team_with_most
        league.save()
