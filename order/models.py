from django.db import models

from users.models import TimeStampModel

class Order(TimeStampModel):
    order_number = models.CharField(max_length=100, unique=True)
    user         = models.ForeignKey('users.User', on_delete=models.CASCADE)
    order_status = models.ForeignKey('OderStatus', on_delete=models.CASCADE)

    class Meta:
        db_table = 'orders'

class OderItem(models.Model):
    user             = models.ForeignKey('user.User', on_delete=models.CASCADE)
    product_option   = models.ForeignKey('products.ProductOption', on_delete=models.CASCADE)
    order            = models.ForeignKey('Order', on_delete=models.CASCADE)
    shippting_status = models.ForeignKey('ShippingStatus', on_delete=models.CASCADE)
    tracking_number  = models.CharField(max_length=45)

    class Meta:
        db_table = 'order_items'

class OderStatus(models.Model):
    status = models.CharField(max_length=45)

    class Meta:
        db_table = 'order_status'

class ShippingStatus(models.Model):
    status = models.CharField(max_length=45)

    class Meta:
        db_table = 'shipping_status'

class Cart(TimeStampModel):
    user          = models.ForeignKey('User', on_delete=models.CASCADE)
    product_option = models.ForeignKey('products.ProductOption', on_delete=models.CASCADE)
    quantity      = models.PositiveIntegerField()

    class Meta:
        db_table = 'carts'