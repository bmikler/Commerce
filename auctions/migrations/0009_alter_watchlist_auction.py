# Generated by Django 3.2.6 on 2021-08-24 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_watchlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='auction',
            field=models.ManyToManyField(blank=True, related_name='watchlist', to='auctions.AuctionList'),
        ),
    ]
