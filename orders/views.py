import json, uuid

from django.http      import JsonResponse, HttpResponse
from django.views     import View
from django.db        import transaction
from django.db.models import F, Sum
from django.utils     import timezone

from .models import (
    Cart,
    Order,
    OrderStatus,
    OrderItem,
    OrderStatusEnum,
    ShippingStatus,
    ShipptingStatusEnum
    )
from users.utils     import login_decorator
from products.models import ProductOption

class OrderView(View):
    @login_decorator
    @transaction.atomic
    def post(self, request):
        user = request.user

        product_options = ProductOption.objects.filter(cart__user=user)\
                                               .prefetch_related('cart_set')\
                                               .annotate(total_quantity=Sum('cart__quantity'))

        sold_out = [
            {
                'product_name': product_option.product.name
            }
            for product_option in product_options 
            if product_option.stock - product_option.cart_set.get(user=user).quantity < 0
        ]
        
        if sold_out: 
            return JsonResponse(
                    {
                        'message' : 'OUT_OF_STOCK',
                        'sold_out': sold_out
                    }, status=202)

        total_payment = product_options.aggregate(total=Sum(F('cart__quantity') * F('price')))['total']

        if user.point - total_payment < 0:
            return JsonResponse({'message': 'LACK_OF_POINT'}, status=202)

        for product_option in product_options:
            product_option.stock -= product_option.total_quantity
        
        ProductOption.objects.bulk_update(product_options, ['stock'])

        order = Order.objects.create(
            order_number = uuid.uuid4(),
            user         = user,
            order_status = OrderStatus.objects.get(id=OrderStatusEnum.COMPLETE.value)
        )

        order_items = [
            OrderItem(
                user             = user,
                product_option   = product_option,
                order            = order,
                shipping_status  = ShippingStatus.objects.get(id=ShipptingStatusEnum.PREPARING_DELIVERY.value),
                quantity         = product_option.cart_set.get(user=user).quantity
            ) for product_option in product_options
        ]
        
        OrderItem.objects.bulk_create(order_items)

        user.point = F('point') - total_payment
        user.save()

        Cart.objects.filter(user=user).delete()
        return HttpResponse(status=201)

    def patch(self, request, order_item_id):
        order_items = OrderItem.objects.filter(id=order_item_id)
        order_item = order_items[0]
        
        if (timezone.now() - order_item.order.created_at).days > 7:
            return JsonResponse({'message': 'NOT_AVAILABLE'}, status=400)
        
        with transaction.atomic():
            total_payment = order_items.aggregate(
                total = Sum(F('quantity') * F('product_option__price'))
                )['total']

            order_items.update(
                shipping_status = ShippingStatus.objects.get(id=ShipptingStatusEnum.PREPARING_DELIVERY.value)
                )
            
            order_item.order.order_status_id = OrderStatus.objects.get(id=OrderStatusEnum.COMPLETE.value)
            order_item.product_option.stock += order_item.quantity
            order_item.user.point           += total_payment

            order_item.order.save()
            order_item.product_option.save()
            order_item.user.save()
        
        return HttpResponse(status=200)
    
    @login_decorator
    def get(self, request):
        orders = Order.objects.filter(user=request.user)

        if not orders.exists():
            return JsonResponse({'message': 'NO_ORDER'}, status=200)

        result = [
            {
                'order_number' : order.order_number,
                'order_status' : order.order_status.name,
                'created_at'   : order.created_at,
                'items' : 
                [
                    {
                        'product_name'   : order_item.product_option.product.name,
                        'color'          : order_item.product_option.color.name if order_item.product_option.color else None,
                        'size'           : order_item.product_option.size.name if order_item.product_option.size else None,
                        'quantity'       : order_item.quantity,
                        'tracking_number': order_item.tracking_number if order_item.tracking_number else None,
                        'shipping_status': order_item.shipping_status.name,
                        'total_price'    : order_item.quantity * order_item.product_option.price,
                        'default_image'  : order_item.product_option.product.default_image,
                        } for order_item in OrderItem.objects.filter(order=order)
                ]
            } for order in orders
        ]

        return JsonResponse({'result': result}, status=200)

class CartView(View):
    @login_decorator
    def delete(self, request, product_option_id):
        Cart.objects.filter(
            user           = request.user,
            product_option = product_option_id
            ).delete()

        return HttpResponse(status=204)
    
    @login_decorator
    def get(self, request):
        carts   = Cart.objects.filter(user=request.user)

        if not carts.exists():
            return JsonResponse({'message': 'NO_PRODUCT'}, status=200)

        result = [
            {
                'product_option_id' : cart.product_option.id,
                'name'              : cart.product_option.product.name,
                'type'              : cart.product_option.product.type.name,
                'color'             : cart.product_option.color.name if cart.product_option.color else None,
                'size'              : cart.product_option.size.name if cart.product_option.size else None,
                'quantity'          : cart.quantity,
                'price'             : cart.product_option.price,
                'total_price'       : cart.quantity * cart.product_option.price,
                'default_image'     : cart.product_option.product.default_image
            } for cart in carts
        ]
            
        return JsonResponse({'result':result}, status=200)

    @login_decorator
    def post(self, request, product_option_id):
        data = json.loads(request.body)
        try:
            quantity = data['quantity']
            
            cart, created = Cart.objects.get_or_create(
                    product_option = ProductOption.objects.get(id=product_option_id),
                    user           = request.user,
                    defaults       = {'quantity': quantity}
                    )

            if not created:
                cart.quantity += quantity
                cart.save()
                return HttpResponse(status=204)
                
            return HttpResponse(status=201)
        except ProductOption.DoesNotExist:
            return JsonResponse({'message': 'INVALID_PRODUCT_OPTION'}, status=400)

    @login_decorator
    def patch(self, request, product_option_id):
        data     = json.loads(request.body)
        quantity = data['quantity']

        cart = Cart.objects.filter(user=request.user, product_option=product_option_id)

        if quantity == '0':
            cart.delete()
            return HttpResponse(status=204)

        cart.update(quantity=quantity)

        return HttpResponse(status=200)
