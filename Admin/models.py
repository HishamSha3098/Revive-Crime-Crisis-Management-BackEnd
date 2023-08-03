from django.db import models
from api.models import ReviveUser

# Create your models here.
class CrisisManage(models.Model):
    user = models.ForeignKey(ReviveUser, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='user_images', null=True, blank=True)
    donation_goal = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    recived_amount = models.DecimalField(max_digits=10,default=0, decimal_places=2,null=True, blank=True)
    date_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    document = models.FileField(upload_to='files/')

    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    


class EventManage(models.Model):

    title = models.CharField(max_length=255, null=True, blank=True)
    place = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='user_images', null=True, blank=True)
    Date_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    description = models.TextField(null=True, blank=True)
    latitude = models.CharField(max_length=255, null=True, blank=True)
    longitude = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title
    

class GalleryManage(models.Model):

    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='user_images', null=True, blank=True)
    Date_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    

    def __str__(self):
        return self.title
    



class Wallet(models.Model):
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Wallet (Balance: {self.balance})"



