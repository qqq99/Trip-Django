from django.contrib import admin

from . import models


class TeamMemberInline(admin.TabularInline):
    model = models.TeamMember


admin.site.register(models.Team)
