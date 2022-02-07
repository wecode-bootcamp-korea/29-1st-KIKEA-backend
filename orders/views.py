import json

from django.http  import JsonResponse, HttpResponse
from django.views import View

from .models     import Order, OrderItem, Cart
from users.utils import login_decorator

class OrderView(View):
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
    def patch(self, request, product_option_id):
        data = json.loads(request.body)

        user_id  = request.user.id
        quantity = data['quantity']

        cart = Cart.objects.filter(user=user_id, product_option=product_option_id)

        if quantity == '0':
            cart.delete()
            return HttpResponse(status=204)

        cart.update(quantity=quantity)

        return HttpResponse(status=200)
