# Generated by Django 3.2.6 on 2021-08-26 17:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_auctionlist_winner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auctionlist',
            name='winner',
        ),
    ]