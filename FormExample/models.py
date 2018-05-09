from django.db import models
from django.contrib.auth.models import User

class Contest(models.Model):
    sport = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    style = models.CharField(max_length=200)
    entryfee = models.IntegerField(default=0)
    totalprizes = models.IntegerField(default=0)
    entry = models.IntegerField(default=0)
    entries = models.IntegerField(default=0)
    live = models.DateTimeField('time contest finishes')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Contest"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)

class Stock(models.Model):
    sector = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    shares = models.IntegerField(default=0)
    pps = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "Stock"

class StockEntry(models.Model):
    sector = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    shares = models.IntegerField(default=0)
    pps = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "StockEntry"
        
class Request(StockEntry):
    entryfee = models.IntegerField(default=0)
    contestlength = models.IntegerField(default=0)
    user = models.ForeignKey(User, unique=True)