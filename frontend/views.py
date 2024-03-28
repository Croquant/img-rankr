import random

from django.db.models import F, Sum
from django.shortcuts import render

from elo.models import Elo


def match_view(request):
    total_games = Elo.objects.aggregate(total_games=Sum("n_games"))[
        "total_games"
    ]
    elo_with_weights = Elo.objects.annotate(
        weight=float(total_games) / max(F("n_games"), 1)
    )
    selected_images = random.choices(
        elo_with_weights, weights=[elo.weight for elo in elo_with_weights], k=2
    )
    img1 = selected_images[0].image
    img2 = selected_images[1].image
    context = {"title": "Match", "img1": img1, "img2": img2}
    return render(request, "match.html", context)
