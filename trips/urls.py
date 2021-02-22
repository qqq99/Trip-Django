from django.conf.urls import url

from . import views

app_name = 'trips'

urlpatterns = [
    url(r"^$", views.TripList.as_view(), name="all"),
    url(r"new/$", views.CreateTrip.as_view(), name="create"),
    url(r"by/(?P<username>[-\w]+)/$",
        views.UserTrips.as_view(), name="for_user"),
    url(r"by/(?P<username>[-\w]+)/(?P<pk>\d+)/$",
        views.TripDetail.as_view(), name="single"),
    url(r"delete/(?P<pk>\d+)/$", views.DeleteTrip.as_view(), name="delete"),
]
