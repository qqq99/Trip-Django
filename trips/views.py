from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy
from django.http import Http404
from django.views import generic

from braces.views import SelectRelatedMixin

from . import forms
from . import models

from django.contrib.auth import get_user_model
User = get_user_model()

class TripList(SelectRelatedMixin, generic.ListView):
    model = models.Trip
    select_related = ("user", "team")


class UserTrips(generic.ListView):
    model = models.Trip
    template_name = "trips/user_trip_list.html"

    def get_queryset(self):
        try:
            self.trip_user = User.objects.prefetch_related("trips").get(
                username__iexact=self.kwargs.get("username")
            )
        except User.DoesNotExist:
            raise Http404
        else:
            return self.trip_user.trips.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["trip_user"] = self.trip_user
        return context


class TripDetail(SelectRelatedMixin, generic.DetailView):
    model = models.Trip
    select_related = ("user", "team")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            user__username__iexact=self.kwargs.get("username")
        )


class CreateTrip(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    fields = ("location","category","number","cost","receipt","date",'reason', 'team')
    model = models.Trip

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class DeleteTrip(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.Trip
    select_related = ("user", "team")
    # go back to all the trips page
    success_url = reverse_lazy("trips:all")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Trip Deleted")
        return super().delete(*args, **kwargs)
