from django.db import models
from .product import Products

class AdImage(models.Model):

    image = models.ImageField(upload_to='uploads/ad/images/')

