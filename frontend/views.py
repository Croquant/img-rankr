import random

from django.core.paginator import Paginator
from django.db.models import Case, F, FloatField, Sum, When
from django.shortcuts import render

from common.utils import encrypt_payload
from elo.models import Elo


def get_division():
    ordered_records = Elo.objects.order_by("-score")

    divisions = Paginator(
        ordered_records, per_page=10, orphans=3, allow_empty_first_page=False
    )

    total_divisions = divisions.num_pages
    chosen_division = random.randint(1, total_divisions)

    return divisions.get_page(chosen_division).object_list


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

    while True:
        selected_images = random.choices(
            elo_with_weights,
            weights=weights,
            k=2,
        )
        if selected_images[0] != selected_images[1]:
            break

    img1 = selected_images[0].image
    img2 = selected_images[1].image
    payload = encrypt_payload((img1.id, img2.id))
    context = {
        "title": "Match",
        "img1": img1,
        "img2": img2,
        "payload": payload,
    }
    return render(request, "match.html", context)
