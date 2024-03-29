import math
import random

from django.db.models import Case, F, FloatField, Sum, When
from django.shortcuts import render

from elo.models import Elo


def get_division():
    ordered_records = Elo.objects.order_by("score")
    total_records = ordered_records.count()
    n = math.floor(total_records / 10)

    total_records = ordered_records.count()
    section_size = math.ceil(total_records / n)

    section_indices = [
        (i * section_size, (i + 1) * section_size) for i in range(n)
    ]

    selected_section = random.randint(0, n - 1)
    start, end = section_indices[selected_section]

    return ordered_records[start:end]


def match_view(request):
    queryset = get_division()
    total_games = max(
        queryset.aggregate(total_games=Sum("n_games"))["total_games"], 1
    )
    elo_with_weights = queryset.annotate(
        weight=Case(
            When(n_games__gt=0, then=float(total_games) / F("n_games")),
            default=total_games,
            output_field=FloatField(),
        )
    )
    weights = [elo.weight for elo in elo_with_weights]
    same = True
    while same:
        selected_images = random.choices(
            elo_with_weights,
            weights=weights,
            k=2,
        )
        if selected_images[0] != selected_images[1]:
            same = False

    img1 = selected_images[0].image
    img2 = selected_images[1].image

    context = {"title": "Match", "img1": img1, "img2": img2}
    return render(request, "match.html", context)
