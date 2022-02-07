from django.http  import JsonResponse
from django.views import View

from .models     import Cart
from users.utils import login_decorator

class CartView(View):
    @login_decorator
    def get(self, request):
        carts   = Cart.objects.filter(user=1)

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