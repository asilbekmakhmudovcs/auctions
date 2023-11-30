from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    pass

class Bids(models.Model):
    bidder = models.ForeignKey(User, related_name="bids", on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    bidding_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}: {self.bidder.username}: {self.bid_amount}'



class Product(models.Model):
    title = models.CharField(max_length=64)
    owner = models.ForeignKey(User, related_name="listings", on_delete=models.CASCADE)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    highest_bid = models.ForeignKey(Bids, related_name="products", on_delete=models.PROTECT, blank=True, null=True)
    
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('clothing', 'Clothing'),
        ('furniture', 'Furniture'),
        ('books', 'Books'),
        ('beauty', 'Beauty & Personal Care'),
        ('home', 'Home & Kitchen'),
        ('toys', 'Toys & Games'),
        ('sports', 'Sports & Outdoors'),
        ('jewelry', 'Jewelry & Watches'),
        ('food', 'Food & Grocery'),
        ('automotive', 'Automotive'),
        ('health', 'Health & Wellness'),
        ('pets', 'Pet Supplies'),
        ('tools', 'Tools & Home Improvement'),
        ('office', 'Office Products'),
        # Add more categories as needed
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, blank=True, ) # TODO: give default
    picture = models.ImageField(upload_to='product_pictures/')
    time_added = models.DateTimeField(auto_now_add=True)
    on_market = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.category}: {self.title}"

    # getting highest bid funciton
    def get_highest_bid_amount(self):
        highest_bid_amount = 0.00  # Default value if there's no bid yet

        # Retrieve all bids associated with this product
        all_bids = Bids.objects.filter(products=self)

        if all_bids.exists():
            highest_bid_amount = max(all_bids.values_list('bid_amount', flat=True))

        return highest_bid_amount
    




class Comments(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


