from django.db.models.signals import post_save
from django.dispatch import receiver

from elo.models import Elo

from .models import Image


@receiver(post_save, sender=Image)
def create_elo_for_image(sender, instance, created, **kwargs):
    """
    Signal handler to create an Elo instance for a new Image.
    """
    if created:
        Elo.objects.get_or_create(image=instance)
