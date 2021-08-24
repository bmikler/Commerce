from auctions.models import Article, AuctionList, Category, Comment
from django.contrib import admin

from .models import *

# Register your models here.


admin.site.register(User)
admin.site.register(Category)
admin.site.register(Article)
admin.site.register(AuctionList)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Watchlist)

