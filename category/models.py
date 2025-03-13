from django.db import models
from autoslug import AutoSlugField
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(max_length=100, unique=True, populate_from='name')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='photos/category')

    def __str__(self):
        return self.name
    

    def get_url(self):
        return reverse('product_slug',args=[self.slug])