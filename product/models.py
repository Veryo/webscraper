from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    avg_stars = models.FloatField(default=0)
    def __str__(self):
        return self.name
    
class Opinions(models.Model):
    opinion_id = models.CharField(max_length=200,default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    recommended = models.CharField(max_length=200)
    stars = models.CharField(max_length=200)
    trust = models.CharField(max_length=200)
    opinion_date = models.CharField(max_length=200)
    buy_date = models.CharField(max_length=200)
    useful_counter = models.IntegerField(max_length=200)
    unuseful_counter = models.IntegerField(max_length=200)
    opinion_desc = models.TextField()
    pros = models.TextField()
    cons = models.TextField()
    amount_pros = models.IntegerField(default=0)
    amount_cons = models.IntegerField(default=0)
