import random, string, json

from django.http  import HttpResponse, JsonResponse
from django.views import View
from django.db    import transaction

from .models         import Cart, Order, OrderStatus, OrderItem, ShippingStatus
from products.models import ProductOption
from users.models    import User

class OrderView(View):
    def post(self, request):
        # user_id       = request.user.id
        data = json.loads(request.body)
        user_id = data['user_id']
        carts         = Cart.objects.filter(user=user_id)
        total_payment = 0

        try:
            with transaction.atomic():
                product_options = []

                for cart in carts:
                    product_option = ProductOption.objects.get(id=cart.product_option.id)

                    if product_option.stock - cart.quantity < 0:
                        raise OutOfStock
                    
                    total_payment        += (cart.quantity * product_option.price)
                    product_option.stock -= cart.quantity
                    product_options.append(product_option)

                user = User.objects.get(id=user_id)

                if user.point - total_payment < 0:
                    raise LackOfPoint
                
                order_number = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

                while Order.objects.filter(order_number=order_number).exists():
                    order_number = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

                order = Order.objects.create(
                    order_number = order_number,
                    user         = user,
                    order_status = OrderStatus.objects.get(id=2)
                )
                
                order_items = []

                for product_option, cart in zip(product_options, carts):
                    order_items.append(OrderItem(
                            user             = user,
                            product_option   = product_option,
                            order            = order,
                            shippting_status = ShippingStatus.objects.get(id=1),
                            quantity         = cart.quantity
                        ))

                user.point -= total_payment
                user.save()

                for product_option in product_options:
                    product_option.save()
                for order_item in order_items:
                    order_item.save()

                # carts.delete()
                return HttpResponse(status=201)
        except OutOfStock:
            return JsonResponse(
                        {
                            'message': 'OUT_OF_STOCK'
                            # 'product_option_id': product_option.id
                            },
                            status=202)
        except LackOfPoint as e:
            return JsonResponse({'message': 'LACK_OF_POINTS'}, status=202)
            
class OutOfStock(Exception):
    def __init__(self):
        super().__init__('OUT_OF_STOCK')

class LackOfPoint(Exception):
    def __init__(self):
        super().__init__('LACK_OF_POINTS')