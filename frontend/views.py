import random

from django.shortcuts import render

from image.models import Image


def test(request):
    ids = Image.objects.values_list("id", flat=True)
    ids = list(ids)
    rand_ids = random.sample(ids, 2)
    images = Image.objects.filter(id__in=rand_ids)
    img1 = images[0]
    img2 = images[1]
    context = {"title": "test", "img1": img1, "img2": img2}
    # if request.method == "POST":
    #     data = request.POST
    #     winner = Img.objects.get(pk=data.get("winner"))
    #     loser = Img.objects.get(pk=data.get("loser"))
    #     Match(winner=winner, loser=loser).save()
    return render(request, "match.html", context)


# def test(request):
#     tag_slug = request.GET.get("tag")
#     tag = ""
#     if not tag_slug:
#         tag = Tag.objects.order_by("?")[0]
#     else:
#         tag = Tag.objects.get(slug=tag_slug)

#     query = Img.objects.filter(tags__slug=tag.slug)
#     images = query.order_by("n_matches", "score")
#     i1 = random.randint(0, 3)
#     i2 = random.randint(i1 + 1, i1 + 10)
#     img1 = images[i1]
#     img2 = images[i2]
#     context = {"title": "test", "img1": img1, "img2": img2}
#     if request.method == "POST":
#         data = request.POST
#         winner = Img.objects.get(pk=data.get("winner"))
#         loser = Img.objects.get(pk=data.get("loser"))
#         Match(winner=winner, loser=loser).save()
#     return render(request, "match.html", context)
