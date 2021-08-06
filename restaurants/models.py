from django.db import models
from django.db.models.fields import related
from login_reg_app.models import User
from django.core.files import File
from urllib import request
import os

class Category(models.Model):
    title = models.CharField(max_length=225)
    alias = models.SlugField(default=None)

    def __str__(self):
        return self.title

    @property
    def get_restaurants(self):
        return Restaurant.objects.filter(category=self.title)

class TransactionType(models.Model):
    title = models.CharField(max_length=45)

    def __str__(self):
        return self.title

    @property
    def get_restaurants(self):
        return Restaurant.objects.filter(transaction_types=self.title)

class Location(models.Model):
    address1 = models.CharField(max_length=100, null=True, blank=True, default=None)
    city = models.CharField(max_length=45)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=45)
    state = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.address1}, {self.city}, {self.state} {self.zip_code}"


class Restaurant(models.Model):
    creator = models.ForeignKey(User, related_name='restaurant_creator', on_delete=models.CASCADE)
    name = models.CharField(max_length=45)
    alias = models.SlugField()
    # image = models.ImageField(upload_to="images")
    image_url = models.URLField(null=True, default=None)
    is_closed = models.BooleanField()
    url = models.CharField(max_length=255)
    review_count = models.IntegerField()
    categories = models.ManyToManyField(Category, related_name="Category")
    rating = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    transaction_types = models.ManyToManyField(TransactionType, related_name='restaurant_transactions')
    price = models.CharField(max_length=5)
    location = models.OneToOneField(Location, null=True, default=None, related_name="restaurant_location", on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    favorites = models.ManyToManyField(User, related_name='favorites')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def get_remote_image(self):
        if self.image_url and not self.image:
            result = request.urlretrieve(self.image_url)
            self.image.save(
                    os.path.basename(self.image_url),
                    File(open(result[0], 'rb'))
                    )
            self.save()

class Review(models.Model):
    creator = models.ForeignKey(User, related_name="user_reviews", on_delete=models.CASCADE)
    title = models.CharField(max_length=45)
    desc = models.TextField()
    restaurant = models.ForeignKey(Restaurant, related_name='restaurant_reviews', on_delete=models.CASCADE)
    rating = models.IntegerField()
    likes = models.ManyToManyField(User, related_name='user_review_likes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.creator.first_name} {self.creator.last_name}"

class Message(models.Model):
    creator = models.ForeignKey(User, related_name="creator_message", on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name="receiver_message", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
