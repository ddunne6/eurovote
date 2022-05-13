from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from .models import Rating, Country
from django.http import Http404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

class RatingMixin(LoginRequiredMixin):
    def set_country(self, country_id):
        print("country set")
        self.country = Country.objects.get(id=country_id)

    def get_urlquery(self,request):
        self.set_country(int(request.GET.get('country')))

    def form_valid(self, form):
        self.get_urlquery(self.request)
        form.instance.voter = self.request.user
        form.instance.country = self.country
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        self.get_urlquery(request)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        self.get_urlquery(self.request)
        context = super().get_context_data(**kwargs)
        context['country_name'] = self.country.name
        return context

    def get_success_url(self):
        success_message = "Vote submitted! " + str(self.object.score) + "/10 for " + str(self.object.country)
        messages.add_message(self.request, messages.SUCCESS, success_message)
        return reverse('my_ratings') 

class CreateRating(RatingMixin, CreateView):
    model = Rating
    fields = ['score']
    template_name = 'app_ratings/rate.html'

class EditRating(RatingMixin, UpdateView):
    model = Rating
    fields = ['score']
    template_name = 'app_ratings/rate.html'

#Get all countries, if rating relation ship assign, else (-)
class MyRatings(LoginRequiredMixin, ListView):
    model = Rating
    template_name = 'app_ratings/my_ratings.html'

    def get_queryset(self, **kwargs):
        query = super().get_queryset(**kwargs)
        query = query.filter(voter=self.request.user)
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = self.get_countries_ratings(context['object_list'])
        return context

    def get_countries_ratings(self, ratings):
        countries = Country.objects.all()
        ratings_combined = []
        for country in countries:
            if ratings.filter(country=country).exists():
                ratings_combined.append({
                    "rating":ratings.filter(country=country),
                    "country": country
                })
            else:
                ratings_combined.append({
                    "rating":'-',
                    "country": country
                })
        return ratings_combined

class AllRatings(LoginRequiredMixin, ListView):
    model = Rating
    template_name = 'app_ratings/all_ratings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = self.get_all_ratings(context['object_list'])
        context['voters'] = self.get_users()
        return context

    def get_all_ratings(self, ratings):
        countries = sorted(Country.objects.all(), key=lambda t: t.average_score, reverse=True)
        users = self.get_users()
        ratings_combined = []
        for country in countries:
            ratings_combined.append({
                'country':country,
                'scores': []
            })
            for user in users:
                if ratings.filter(voter=user, country=country).exists():
                    ratings_combined[-1]["scores"].append(ratings.filter(voter=user, country=country))
                else:
                    ratings_combined[-1]["scores"].append('-')
        #print(ratings_combined)
        return ratings_combined

    def get_users(self):
        return User.objects.all()
