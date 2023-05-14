from typing import List
from django.views.generic.edit import FormView
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from .models import Rating, Country
from django.http import Http404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from app_ratings.forms import RateCountryForm


class RatingMixin(LoginRequiredMixin):
    template_name = 'app_ratings/rate.html'

    def set_country(self, country_id):
        self.country = Country.objects.get(id=country_id)

    def get_urlquery(self, request):
        self.set_country(int(request.GET.get('country')))

    def form_valid(self, form):
        self.get_urlquery(self.request)
        form.instance.voter = self.request.user
        form.instance.country = self.country
        self.object = form.save()
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        self.get_urlquery(request)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        self.get_urlquery(self.request)
        context = super().get_context_data(**kwargs)
        context['country_name'] = f"{self.country.country.name}"
        return context

    def get_success_url(self):
        success_message = "Vote submitted! " + \
            str(self.object.score) + "/10 for " + \
            str(self.object.country.country.name)
        messages.add_message(self.request, messages.SUCCESS, success_message)
        return reverse('my_ratings')


class CreateRating(RatingMixin, FormView):
    form_class = RateCountryForm


class EditRating(RatingMixin, UpdateView):  # FIXME
    model = Rating
    fields = ['score']

    def get_success_url(self):
        success_message = "Vote updated! " + \
            str(self.object.score) + "/10 for " + \
            str(self.object.country.country.name)
        messages.add_message(self.request, messages.SUCCESS, success_message)
        return reverse('my_ratings')


class MyRatings(LoginRequiredMixin, ListView):
    model = Rating
    template_name = 'app_ratings/my_ratings.html'

    def get_queryset(self, **kwargs):
        query = super().get_queryset(**kwargs)
        query = query.filter(voter=self.request.user)
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = self.get_countries_ratings(
            context['object_list'])
        return context

    def get_countries_ratings(self, ratings):
        countries = Country.objects.all()
        ratings_combined = []
        for country in countries:
            if ratings.filter(country=country).exists():
                ratings_combined.append({
                    "rating": ratings.filter(country=country),
                    "country": country
                })
            else:
                ratings_combined.append({
                    "rating": '-',
                    "country": country
                })
        return ratings_combined

class AllRatings(LoginRequiredMixin, ListView):
    model = Rating
    template_name = 'app_ratings/all_ratings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = self.get_all_ratings()
        return context

    def get_all_ratings(self):
        ratings: List[Rating] = Rating.objects.all()
        countries: List[Country] = sorted(Country.objects.all(), key=lambda t: t.average_score, reverse=True)
        users: List[User] = User.objects.all()
        table_data = []

        for country in countries:
            table_data.append(self.get_table_data_row(country))
            country_ratings = ratings.filter(country=country)
            for user in users:
                if country_ratings.filter(voter=user).exists():
                    table_data[-1][user.username] = country_ratings.filter(
                        voter=user).first().score
                else:
                    table_data[-1][user.username] = "-"

        return table_data
    
    def get_table_data_row(self, country: Country):
        return {"Running Order": f"{country.running_order}", "Country": f"{country.country.name}",
                               "Average Score": country.average_score}

    def get_users(self):
        return User.objects.all()
    
class ZScoreRatings(AllRatings):
    def get_table_data_row(self, country: Country):
        return {"Running Order": f"{country.running_order}", "Country": f"{country.country.name}",
                               "Z-Score": country.z_score}
