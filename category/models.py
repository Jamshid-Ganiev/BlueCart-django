from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'


    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=400, blank=True)
    image = models.ImageField(upload_to='photos/categories', blank=True)


    def get_url(self):
        return reverse('store:products_by_category', args=[self.slug]) 


    def __str__(self):
        return self.category_name