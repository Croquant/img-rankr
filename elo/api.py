from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from ninja import Router

from common.utils import decrypt_payload
from frontend.views import match_view

from .models import Elo, Match

router = Router()


@router.get(
    "/match",
)
def add_image(request, w: int, p: str):
    try:
        if w not in (0, 1):
            return HttpResponseBadRequest("Invalid Request: w must be 0 or 1.")

        payload = decrypt_payload(p)

        winner_elo = Elo.objects.get(pk=payload[w])
        loser_elo = Elo.objects.get(pk=payload[1 - w])

        Match.objects.create(winner=winner_elo, loser=loser_elo)
        return redirect(match_view)

    except Exception:
        return HttpResponseBadRequest("Invalid Request")
