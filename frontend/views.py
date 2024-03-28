import random

from django.db.models import Case, F, FloatField, Sum, When
from django.shortcuts import render

from elo.models import Elo


def match_view(request):
    total_games = Elo.objects.aggregate(total_games=Sum("n_games"))[
        "total_games"
    ]
    elo_with_weights = Elo.objects.annotate(
        weight=Case(
            When(n_games__gt=0, then=float(total_games) / F("n_games")),
            default=total_games,
            output_field=FloatField(),
        )
    )
    selected_images = random.choices(
        elo_with_weights, weights=[elo.weight for elo in elo_with_weights], k=2
    )
    img1 = selected_images[0].image
    img2 = selected_images[1].image
    context = {"title": "Match", "img1": img1, "img2": img2}
    return render(request, "match.html", context)
