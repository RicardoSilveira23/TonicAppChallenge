from .base import *


class League(BaseModel):
    # Implicit id auto increment field created
    name = models.TextField(unique=True, blank=True, null=False)
    country = models.TextField(blank=True, null=False)
    number_of_teams = models.IntegerField(blank=True, null=False, default=0)
    most_championships = models.ForeignKey(
        "Team",
        on_delete=models.DO_NOTHING,
        related_name="most_championships",
        blank=True,
        null=True,
    )
    most_appearances = models.ForeignKey(
        "Player",
        on_delete=models.DO_NOTHING,
        related_name="most_appearances",
        blank=True,
        null=True,
    )
    current_champion = models.ForeignKey(
        "Team",
        on_delete=models.DO_NOTHING,
        related_name="current_champion",
        blank=True,
        null=True,
    )
