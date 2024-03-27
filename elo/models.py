from django.db import models
from ulid import ULID

from image.models import Image

from .constants import DEFAULT_ELO


class Elo(models.Model):
    image = models.OneToOneField(
        Image, primary_key=True, on_delete=models.CASCADE, related_name="elo"
    )
    score = models.FloatField(default=DEFAULT_ELO)
    n_games = models.PositiveIntegerField(default=0)
    n_wins = models.PositiveIntegerField(default=0)
    n_losses = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Calculate the previous score (if Elo object already exists)
        if self.pk:
            try:
                previous_elo_history = EloHistory.objects.filter(
                    elo=self
                ).latest("timestamp")
                previous_score = previous_elo_history.new_score
            except EloHistory.DoesNotExist:
                previous_score = (
                    DEFAULT_ELO  # Initial score for new Elo objects
                )
        else:
            previous_score = DEFAULT_ELO  # Initial score for new Elo objects

        super().save(*args, **kwargs)  # Save the Elo object

        # Create an associated EloHistory object
        EloHistory.objects.create(
            elo=self,
            previous_score=previous_score,
            new_score=self.score,
        )

    def __str__(self):
        return f"elo({self.image.id})"


class EloHistory(models.Model):
    id = models.CharField(
        primary_key=True, max_length=26, default=ULID, editable=False
    )
    elo = models.ForeignKey(
        Elo, on_delete=models.CASCADE, related_name="history"
    )
    previous_score = models.FloatField()
    new_score = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"elo_history({self.elo.image.id}-{self.id})"
