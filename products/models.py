from django.db   import models
from core.models import TimeStampModel

class ProductOption(TimeStampModel):
    price   = models.PositiveBigIntegerField()
    stock   = models.IntegerField()
    color   = models.ForeignKey('Color', on_delete=models.CASCADE, null=True)
    size    = models.ForeignKey('Size', on_delete=models.CASCADE, null=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'product_options'

class Type(models.Model):
    name         = models.CharField(max_length=45)
    image_url    = models.URLField(max_length=1000)
    sub_category = models.ForeignKey('SubCategory', on_delete=models.CASCADE)

    class Meta:
        db_table = 'types'

class Product(TimeStampModel):
    name          = models.CharField(max_length=45)
    description   = models.TextField(max_length=500)
    default_image = models.URLField(max_length=1000)
    type          = models.ForeignKey('Type', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'products'

class ProductOptionImage(models.Model):
    image_url      = models.URLField(max_length=1000)
    product_option = models.ForeignKey('ProductOption', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'product_option_images'

class TypeImage(models.Model):
    image_url = models.URLField(max_length=1000)
    type      = models.ForeignKey('Type', on_delete=models.CASCADE) 

    class Meta:
        db_table = 'type_images'

class Category(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'categories'

class SubCategory(models.Model):
    name     = models.CharField(max_length=45)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    class Meta:
        db_table = 'sub_categories'

class Review(TimeStampModel):
    comment = models.TextField(max_length=500)
    rating  = models.DecimalField(max_digits=2, decimal_places=1)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    user    = models.ForeignKey('users.User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'reviews'

class Color(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'colors'

class Size(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'sizes'
