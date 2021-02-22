from django.conf import settings
from django.urls import reverse
from django.db import models
from django.utils import timezone
import misaka

from teams.models import Team

from django.contrib.auth import get_user_model
User = get_user_model()


class Trip(models.Model):
    user = models.ForeignKey(User, related_name="trips",
                             on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    category = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    number = models.IntegerField()
    cost = models.IntegerField(default=0)
    receipt = models.ImageField(upload_to='image', default='Desert 3.jpg')
    reason = models.TextField()
    reason_html = models.TextField(editable=False)
    date = models.DateTimeField()
    team = models.ForeignKey(
        Team, related_name="trips", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.category

    def save(self, *args, **kwargs):
        self.reason_html = misaka.html(self.reason)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "trips:single",
            kwargs={
                "username": self.user.username,
                "pk": self.pk
            }
        )

    class Meta:
        ordering = ["-created_at"]
