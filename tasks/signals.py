from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Tag

@receiver(post_migrate)
def create_default_tags(sender, **kwargs):
    if sender.name == "tasks":
        Tag.create_default_tags()