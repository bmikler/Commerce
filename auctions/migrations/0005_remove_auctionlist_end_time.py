# Generated by Django 3.2.6 on 2021-08-22 10:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_rename_start_price_auctionlist_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auctionlist',
            name='end_time',
        ),
    ]
