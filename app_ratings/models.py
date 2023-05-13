from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.db.models import Avg
from django_countries.fields import CountryField
from django.utils.functional import cached_property

class Country(models.Model):
    running_order = models.IntegerField()
    country = CountryField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['running_order'], name='order')
        ]
        ordering = ['running_order']

    def __str__(self):
        return self.country.name

    @cached_property
    def average_score(self):
        avg = Rating.objects.filter(country=self.id).aggregate(Avg('score'))
        avg = avg['score__avg']
        if not avg:
            avg = "-"
        else:
            avg = str(round(avg, 2))
        return avg

class Rating(models.Model):
    score = models.IntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(1)]
    )
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.voter) + " - " + self.country.country.name + " (" + str(self.score) + "/10)"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['voter', 'country'], name='one_vote_per_person')
        ]