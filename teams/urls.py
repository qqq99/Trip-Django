from django.conf.urls import url

from . import views

app_name = 'teams'

urlpatterns = [
    url(r"^$", views.ListTeams.as_view(), name="all"),
    url(r"^new/$", views.CreateTeam.as_view(), name="create"),
    url(r"^trips/in/(?P<slug>[-\w]+)/$",
        views.SingleTeam.as_view(), name="single"),
    url(r"join/(?P<slug>[-\w]+)/$", views.JoinTeam.as_view(), name="join"),
    url(r"leave/(?P<slug>[-\w]+)/$", views.LeaveTeam.as_view(), name="leave"),
]
