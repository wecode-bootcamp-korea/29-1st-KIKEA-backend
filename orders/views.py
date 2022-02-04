import random, string, json

from django.http  import HttpResponse, JsonResponse
from django.views import View
from django.db    import transaction
from django.utils import timezone

from .models import (
    Cart,
    Order,
    OrderStatus,
    OrderItem,
    ShippingStatus
    )
from products.models import ProductOption
from users.models    import User

class OrderView(View):
    def patch(self, request):
        # user_id = request.user.id
        order_id = 9
        user_id = 1
        order = Order.objects.filter(user=user_id, id=order_id)
        
        if (timezone.now() - order[0].created_at).days > 7:
            return JsonResponse({'message': 'NOT_AVAILABLE'}, status=400)
        
        with transaction.atomic():
            order_items = order[0].orderitem_set.filter(order=order[0], user=user_id)

            total_payment = 0

            for order_item in order_items:
                total_payment                   += (order_item.quantity * order_item.product_option.price)
                order_item.product_option.stock += order_item.quantity
                order_item.product_option.save()

            order_items.update(shipping_status_id=5)
            order.update(order_status_id=3)
            user        = User.objects.get(id=user_id)
            user.point += total_payment
            user.save()
        
        return HttpResponse(status=200)  

    def get(self, request):
        # user_id       = request.user.id
        data = json.loads(request.body)
        user_id = data['user_id']

        order_items = OrderItem.objects.filter(user=user_id)

        if not order_items.exists():
            return JsonResponse({'message': 'NO_ORDER'}, status=200)

        result = []

        for order_item in order_items:
            color           = 'NULL'
            size            = 'NULL'
            tracking_number = 'NULL'

            if order_item.product_option.color != None:
                color = order_item.product_option.color.name
            if order_item.product_option.size != None:
                size = order_item.product_option.size.name
            if order_item.tracking_number != None:
                tracking_number = order_item.tracking_number
            
            result.append(
                {   
                    'order_number'   : order_item.order.order_number,
                    'order_status'   : order_item.order.order_status.name,
                    'product_name'   : order_item.product_option.product.name,
                    'color'          : color,
                    'size'           : size,
                    'quantity'       : order_item.quantity,
                    'tracking_number': tracking_number,
                    'shipping_status': order_item.shipping_status.name,
                    'total_price'    : order_item.quantity * order_item.product_option.price,
                    'default_image'  : order_item.product_option.product.default_image,
                    'created_at'     : order_item.order.created_at
                }
            )

        return JsonResponse({'result': result}, status=200)

    def post(self, request):
        # user_id       = request.user.id
        # data = json.loads(request.body)
        user_id = 1
        carts         = Cart.objects.filter(user=user_id)
        total_payment = 0

        try:
            with transaction.atomic():
                product_options = []

                for cart in carts:
                    product_option = ProductOption.objects.get(id=cart.product_option.id)

                    if product_option.stock - cart.quantity < 0:
                        return JsonResponse(
                            {
                                'message'       : 'OUT_OF_STOCK',
                                'product_option': product_option.product.name
                            }, status=202)
                    
                    total_payment        += (cart.quantity * product_option.price)
                    product_option.stock -= cart.quantity
                    product_options.append(product_option)

                user = User.objects.get(id=user_id)

                if user.point - total_payment < 0:
                    # raise LackOfPoint
                    return JsonResponse({'message': 'LACK_OF_POINT'}, status=202)
                
                order_number = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

                while Order.objects.filter(order_number=order_number).exists():
                    order_number = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

                order = Order.objects.create(
                    order_number = order_number,
                    user         = user,
                    order_status = OrderStatus.objects.get(id=2)
                )
                
                # order_items = []

                for product_option, cart in zip(product_options, carts):
                    OrderItem.objects.create(
                            user             = user,
                            product_option   = product_option,
                            order            = order,
                            shipping_status  = ShippingStatus.objects.get(id=1),
                            quantity         = cart.quantity
                        )

                user.point -= total_payment
                user.save()

                for product_option in product_options:
                    product_option.save()
                # for order_item in order_items:
                #     order_item.save()

                # carts.delete()
                return HttpResponse(status=201)
        except KeyError:
            print('hehe')
        # except LackOfPoint as e:
        #     return JsonResponse({'message': str(e)}, status=202)
            
class OutOfStock(Exception):
    def __init__(self):
        super().__init__('OUT_OF_STOCK')

class LackOfPoint(Exception):
    def __init__(self):
        super().__init__('LACK_OF_POINTS')