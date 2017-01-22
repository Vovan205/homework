from django.db import models
from django.utils import timezone


class Post(models.Model):    
    item_name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    description = models.TextField()
    published_date = models.DateTimeField(
            blank=True, null=True)
    img = models.ImageField(upload_to='blog/static')
    commented = models.IntegerField()

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Item_User(models.Model):
    user = models.CharField(max_length=200)
    item = models.IntegerField()
    number = models.IntegerField()
