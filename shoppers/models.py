from django.db import models

# Create your models here.
class Shopper(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=70)
    email = models.EmailField(max_length=254)
    nif = models.CharField(max_length=10)