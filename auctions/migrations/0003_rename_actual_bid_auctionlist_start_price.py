# Generated by Django 3.2.6 on 2021-08-21 13:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auto_20210821_1518'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auctionlist',
            old_name='actual_bid',
            new_name='start_price',
        ),
    ]
