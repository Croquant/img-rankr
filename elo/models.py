from django.db import models
from ulid import ULID

from image.models import Image

from .constants import DEFAULT_ELO


class Elo(models.Model):
    image = models.OneToOneField(
        Image,
        primary_key=True,
        on_delete=models.CASCADE,
        related_name="elo",
        editable=False,
    )
    score = models.FloatField(default=DEFAULT_ELO, editable=False)
    n_games = models.PositiveIntegerField(default=0, editable=False)
    n_wins = models.PositiveIntegerField(default=0, editable=False)
    n_losses = models.PositiveIntegerField(default=0, editable=False)
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
        Elo, on_delete=models.CASCADE, related_name="history", editable=False
    )
    previous_score = models.FloatField(editable=False)
    new_score = models.FloatField(editable=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"elo_history({self.elo.image.id}-{self.id})"


class Match(models.Model):
    id = models.CharField(
        primary_key=True, max_length=26, default=ULID, editable=False
    )

    def __str__(self):
        return f"match({self.id})"

    # -- fields ----------
    k = models.FloatField(blank=True, null=True, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    # -- winner ----------
    winner = models.ForeignKey(
        Elo, on_delete=models.CASCADE, related_name="wins", editable=False
    )
    winner_score_old = models.FloatField(blank=True, null=True, editable=False)
    winner_score_new = models.FloatField(blank=True, null=True, editable=False)
    winner_diff = models.FloatField(blank=True, null=True, editable=False)

    # -- loser ----------
    loser = models.ForeignKey(
        Elo, on_delete=models.CASCADE, related_name="losses", editable=False
    )
    loser_score_old = models.FloatField(blank=True, null=True, editable=False)
    loser_score_new = models.FloatField(blank=True, null=True, editable=False)
    loser_diff = models.FloatField(blank=True, null=True, editable=False)

    def get_k(self):
        total_matches = self.winner.n_games + self.loser.n_games
        return max((800 / (total_matches + 3)), 10)

    def get_diff(self, k: float, w_score: float, l_score: float):
        w_ex = 1 / (10 ** (-(w_score - l_score) / 400) + 1)
        return k * (1 - w_ex)

    def save(self, *args, **kwargs):
        self.k = self.get_k()

        self.winner_score_old = self.winner.score
        self.loser_score_old = self.loser.score

        diff = self.get_diff(self.k, self.winner.score, self.loser.score)
        self.winner_diff = diff
        self.loser_diff = -diff

        self.winner_score_new = self.winner.score + diff
        self.loser_score_new = self.loser.score - diff

        self.winner.score = self.winner_score_new
        self.winner.n_games += 1
        self.winner.n_wins += 1
        self.winner.save()

        self.loser.score = self.loser_score_new
        self.loser.n_games += 1
        self.loser.n_losses += 1
        self.loser.save()

        super().save(*args, **kwargs)
