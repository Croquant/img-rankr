from django.shortcuts import redirect
from ninja import Router

from frontend.views import match_view

from .models import Elo, Match

router = Router()


@router.get(
    "/match",
)
def add_image(request, winner: str, loser: str):
    winner_elo = Elo.objects.get(pk=winner)
    loser_elo = Elo.objects.get(pk=loser)
    Match.objects.create(winner=winner_elo, loser=loser_elo)
    return redirect(match_view)
