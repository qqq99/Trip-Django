from django.contrib import messages
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)

from django.urls import reverse
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404
from django.views import generic
from teams.models import Team, TeamMember
from . import models
from django.views.generic import TemplateView

class CreateTeam(LoginRequiredMixin, generic.CreateView):
    fields = ("name", "team_leader","members","date_created","description")
    model = Team


class SingleTeam(generic.DetailView):
    model = Team


class ListTeams(generic.ListView):
    model = Team

class JoinTeam(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("teams:single", kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):
        team = get_object_or_404(Team, slug=self.kwargs.get("slug"))

        try:
            TeamMember.objects.create(user=self.request.user, team=team)

        except IntegrityError:
            messages.warning(
                self.request, ("Warning, already a member of {}".format(team.name)))

        else:
            messages.success(
                self.request, "You are now a member of the {} team.".format(team.name))

        return super().get(request, *args, **kwargs)


class LeaveTeam(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("teams:single", kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):

        try:

            membership = models.TeamMember.objects.filter(
                user=self.request.user,
                team__slug=self.kwargs.get("slug")
            ).get()

        except models.TeamMember.DoesNotExist:
            messages.warning(
                self.request,
                "You can't leave this team because you aren't in it."
            )
        else:
            membership.delete()
            messages.success(
                self.request,
                "You have successfully left this team."
            )
        return super().get(request, *args, **kwargs)
