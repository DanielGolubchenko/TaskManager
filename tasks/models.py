from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    @classmethod
    def create_default_tags(cls):
        """Creates default tags if they do not exist."""
        default_tags = ["Work", "Studies", "Home", "Meetings", "Goals", "Reading", "Shopping", "Bills"]
        for tag in default_tags:
            cls.objects.get_or_create(name=tag)

class Task(models.Model):
    PRIORITY_CHOICES = [
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
        ("Urgent", "Urgent"),
    ]

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In progress", "In progress"),
        ("Completed", "Completed"),
        ("Canceled", "Canceled"),
    ]

    title = models.CharField(max_length=255)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Low')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Pending')
    description = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.status})"