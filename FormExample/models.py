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

class Request(models.Model):
    id = models.AutoField(primary_key=True)
    stocks = models.ManyToManyField(StockEntry)
    entryfee = models.IntegerField(default=0)
    length = models.IntegerField(default=0)
    user = models.CharField(max_length=200)
    matched = models.BooleanField(default=False)

    def __str__(self):
        return self.user

    class Meta:
        db_table = "Request"

class HeadToHeadMatch(models.Model):
    user1 = models.OneToOneField(Request, on_delete=models.CASCADE, related_name='firstuser')
    user2 = models.OneToOneField(Request,on_delete=models.CASCADE, related_name='seconduser')

    class Meta:
        db_table = "Headtoheadmatch"

