# dashboard/models.py

from django.db import models
from django.conf import settings


class FYPPost(models.Model):
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('closed', 'Closed'),
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='fyp_posts'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    skills_needed = models.CharField(max_length=300, help_text='e.g. Python, React, ML')
    members_needed = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title