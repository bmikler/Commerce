from typing import ItemsView
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE, PROTECT
from django.db.models.fields.related import ForeignKey

class User(AbstractUser):
    pass

class Category(models.Model):
    type = models.CharField(max_length=64)

    def __str__(self) -> str:
        return self.type

class Article(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=600)
    image_url = models.URLField()
    article_category = ForeignKey(Category, on_delete=PROTECT)

    def __str__(self) -> str:
        return self.title

class AuctionList(models.Model):
    seller = ForeignKey(User, on_delete=CASCADE)
    item = ForeignKey(Article, on_delete=CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.id}: {self.item.title} listed by {self.seller}"

class Bid(models.Model):
    buyer = ForeignKey(User, on_delete=CASCADE)
    auction = ForeignKey(AuctionList, on_delete=CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)

class Comment(models.Model):
    author = ForeignKey(User, on_delete=CASCADE)
    auction_comment = ForeignKey(AuctionList, on_delete=CASCADE)
    text = models.CharField(max_length=128)