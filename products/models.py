from django.db              import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models           import TimeStampModel

class ProductOption(TimeStampModel):
    price   = models.PositiveBigIntegerField()
    stock   = models.TextField()
    color   = models.ForeignKey('Color', on_delete=models.CASCADE)
    size    = models.ForeignKey('Size', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'product_options'

class Type(TimeStampModel):
    name        = models.CharField(max_length=45)
    subcategory = models.ForeignKey('SubCategory', on_delete=models.CASCADE)

    class Meta:
        db_table = 'types'

class Product(TimeStampModel):
    name          = models.CharField(max_length=45)
    description   = models.TextField()
    default_image = models.URLField()
    type          = models.ForeignKey('Type', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'products'

class Image(TimeStampModel):
    image_url     = models.URLField(max_length=500)
    productoption = models.ForeignKey('ProductOption', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'images'

class Category(TimeStampModel):
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
    rating  = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    user    = models.ForeignKey('users.User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'reviews'

class Color(TimeStampModel):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'colors'

class Size(TimeStampModel):
    product_size = models.CharField(max_length=45)

    class Meta:
        db_table = 'sizes'
