import random, string, json

from django.http  import HttpResponse, JsonResponse
from django.views import View

from .models         import Cart, Order, OrderStatus
from products.models import ProductOption
from users.models    import User

class OrderView(View):
    def post(self, request):
        # user_id       = request.user.id
        data = json.loads(request.body)
        user_id = data['user_id']
        carts         = Cart.objects.filter(user=user_id)
        total_payment = 0

        for cart in carts:
            product_option = ProductOption.objects.get(id=cart.product_option.id)

            if product_option.stock - cart.quantity < 0:
                return JsonResponse(
                    {
                        'message': 'OUT_OF_STOCK',
                        'product_option_id': product_option.id
                        },
                        status=202)
            
            total_payment        += (cart.quantity * product_option.price)
            product_option.stock -= cart.quantity
            product_option.save()

        user = User.objects.get(id=user_id)

        if user.point - total_payment < 0:
            return JsonResponse({'message': 'LACK_OF_POINTS'}, status=202)
        
        order_number = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

        while Order.objects.filter(order_number=order_number).exists():
            order_number = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

        Order.objects.create(
            order_number = order_number,
            user         = user,
            order_status = OrderStatus.objects.get(id=2)
        )
        
        user.point -= total_payment
        user.save()

        carts.delete()

        return HttpResponse(status=201)