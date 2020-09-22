from django.db import models
from django.contrib.auth.models import User
import numpy as np


class Product(models.Model):
    name = models.CharField(max_length=128, null=True)
    price = models.FloatField()
    image = models.ImageField(null=True, blank=True)

    def average_rating(self):
        all_ratings = list(map(lambda x: x.rating, self.review_set.all()))
        return np.mean(all_ratings)

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        try:
            url = self.image.url
        except Exception:
            url = ''
        return url


class Review(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    pub_date = models.DateTimeField('date published')
    user_name = models.CharField(max_length=128)
    comment = models.CharField(max_length=128)
    rating = models.IntegerField(choices=RATING_CHOICES)

    def __str__(self):
        return self.user_name


class Cluster(models.Model):
    name = models.CharField(max_length=128)
    users = models.ManyToManyField(User)

    def get_members(self):
        return '\n'.join([u.username for u in self.users.all()])

    def __str__(self):
        return self.name
