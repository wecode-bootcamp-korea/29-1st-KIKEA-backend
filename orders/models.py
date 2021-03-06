from enum import Enum

from django.db   import models

from core.models import TimeStampModel

class Order(TimeStampModel):
    order_number = models.CharField(max_length=100, unique=True)
    user         = models.ForeignKey('users.User', on_delete=models.CASCADE)
    order_status = models.ForeignKey('OrderStatus', on_delete=models.CASCADE)

    class Meta:
        db_table = 'orders'

class OrderItem(models.Model):
    user             = models.ForeignKey('users.User', on_delete=models.CASCADE)
    product_option   = models.ForeignKey('products.ProductOption', on_delete=models.CASCADE)
    order            = models.ForeignKey('Order', on_delete=models.CASCADE)
    shipping_status  = models.ForeignKey('ShippingStatus', on_delete=models.CASCADE)
    tracking_number  = models.CharField(max_length=45, null=True, unique=True)
    quantity         = models.IntegerField(null=True)

    class Meta:
        db_table = 'order_items'

class OrderStatus(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'order_status'

class ShippingStatus(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'shipping_status'

class Cart(TimeStampModel):
    user           = models.ForeignKey('users.User', on_delete=models.CASCADE)
    product_option = models.ForeignKey('products.ProductOption', on_delete=models.CASCADE)
    quantity       = models.PositiveIntegerField()

    class Meta:
        db_table = 'carts'

class OrderStatusEnum(Enum):
    PANDING              = 1
    COMPLETE             = 2
    CANCELLED            = 3
    PARTIAL_CANCELLATION = 5

class ShipptingStatusEnum(Enum):
    PREPARING_DELIVERY = 1
    IN_TRANSIT         = 2
    SHIPPING           = 3
    DELIVERED          = 4
    RETURN_REQUEST     = 5
    RETRIEVING         = 6
    SHIPMENT_RETURNED  = 7