# Generated by Django 4.2.7 on 2023-11-23 21:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_remove_product_current_highest_bid_product_bids'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='bids',
        ),
        migrations.AddField(
            model_name='product',
            name='highest_bid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='products', to='auctions.bids'),
        ),
    ]