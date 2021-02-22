from django import template
from django.db import models
# just allows us to remove any characters that are alphanumerics or underscores or hyphens and basically the idea behind that is if you have a string that has spaces in it and you want to use that as part of your URL it's going to be able to lowercase and add dashes instead of spaces.
from django.utils.text import slugify
# misaka allows us to actually do Lincoln betting.If you've ever use something like redit commenting system you can actually put links are a little bit a mark down text that that's what Misaka actually doee
import misaka
from django.urls import reverse
from django.utils import timezone
# Get user model returns the user model that's currently active in this project.
from django.contrib.auth import get_user_model
# allows us to do: E.G. call things off of the current user's session
User = get_user_model()
# this is how we can use custom template tags in the future.
register = template.Library()


class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    team_leader = models.CharField(max_length=255)
    members = models.ManyToManyField(User, through="TeamMember")
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=False, default='', blank=True)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.description_html = misaka.html(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("teams:single", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["name"]


class TeamMember(models.Model):
    team = models.ForeignKey(
        Team, related_name='memberships', on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, related_name='user_teams', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('team', 'user')
