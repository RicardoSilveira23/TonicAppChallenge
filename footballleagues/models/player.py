from .base import *
from .team import *


class Player(BaseModel):
    # Implicit id auto increment field created
    name = models.TextField(db_index=True, blank=True, null=False)
    age = models.IntegerField(blank=True, null=False)
    position = models.TextField(blank=True, null=False)
    appearances = models.IntegerField(blank=True, null=False)
    team = models.ForeignKey(
        Team,
        on_delete=models.DO_NOTHING,
        related_name="players",
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
        new_team = instance.team
        current_team = player.team
        # No team -> new team
        if current_team == None and new_team != None:
            new_team.number_of_players += 1
            new_team.save()
            compare_most_appearances(new_team, instance)

        # Team -> no team
        elif current_team != None and new_team == None:
            current_team.number_of_players -= 1
            current_team.save()
            query_most_appearances(current_team, instance)

        # Changed Team
        elif not current_team == new_team:
            current_team.number_of_players -= 1
            current_team.save()
            query_most_appearances(current_team, instance)

            new_team.number_of_players += 1
            new_team.save()
            compare_most_appearances(new_team, instance)

        # Changed number of appearances but remained in same team
        elif current_team == new_team and player.appearances != instance.appearances:
            compare_most_appearances(current_team, instance)


# POST_SAVE - check if player is being deleted or if new add to team player count
@receiver(post_save, sender=Player)
def new_or_deleted_team_player(sender, instance, created, **kwargs):
    team = instance.team
    if team is not None:
        if created:
            team = instance.team
            team.number_of_players += 1
            team.save()
            compare_most_appearances(team, instance)

        elif instance.is_deleted:
            team.number_of_players -= 1
            team.save()
            query_most_appearances(team, instance)


def compare_most_appearances(team, player):
    if team.league is not None:
        # if team has a league its required to calculate most_appearances field
        if team.league.most_appearances is not None:
            if team.league.most_appearances.appearances < player.appearances:
                team.league.most_appearances = player
                team.league.save()
        else:
            team.league.most_appearances = player
            team.league.save()


def query_most_appearances(team, player):
    if team.league.most_appearances == player:
        # query most_appearances
        league_teams = Team.objects.filter(is_deleted=False, league=team.league)
        player_with_most = (
            Player.objects.filter(is_deleted=False, team__in=league_teams)
            .exclude(id=player.id)
            .order_by("-appearances")
            .first()
        )
        team.league.most_appearances = player_with_most
        team.league.save()
