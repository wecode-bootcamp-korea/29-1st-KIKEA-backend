from django.http  import JsonResponse
from django.views import View

from .models import Cart

class CartView(View):
    def get(self, request):
        user_id = request.user.id
        carts   = Cart.objects.filter(user=user_id)

        if not carts.exists():
            return JsonResponse({'message': 'NO_PRODUCT'}, status=200)

        result = []

        for cart in carts:
            color = 'NULL'
            size  = 'NULL'

            if cart.product_option.color != None:
                color = cart.product_option.color.name
            if cart.product_option.size != None:
                size = cart.product_option.size.name

            result.append(
                {
                    'name'         : cart.product_option.product.name,
                    'type'         : cart.product_option.product.type.name,
                    'color'        : color,
                    'size'         : size,
                    'quantity'     : cart.quantity,
                    'price'        : cart.product_option.price,
                    'default_image': cart.product_option.product.default_image
                }
            )

        return JsonResponse({'result':result}, status=200)