from django.db import models

# Model for products
class Product(models.Model):
    LIVE = 1
    DELETE = 0
    DELETE_CHOICES = ((LIVE,'live'),(DELETE,'delete'))

    title = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    description = models.TextField(max_length=200)
    product_image = models.ImageField(upload_to='products/')

    priority = models.IntegerField(default=0)
    delete_status = models.IntegerField(choices=DELETE_CHOICES,default=LIVE,db_index=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self)->str:
        return self.title
    
