import json

from django.http  import HttpResponse, JsonResponse
from django.views import View

from .models         import Cart
from users.models    import User
from products.models import ProductOption

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

    def post(self, request):
        data = json.loads(request.body)

        try:
            quantity = 1

            user           = User.objects.get(id=request.user.id)
            product_option = ProductOption.objects.get(id=data['product_option_id'])
            cart           = Cart.objects.filter(user=user.id, product_option=product_option.id)
            
            if cart.exists():
                quantity += cart[0].quantity
                cart.update(quantity=quantity)

                return HttpResponse(status=204)

            Cart.objects.create(
                quantity       = quantity,
                product_option = product_option,
                user           = user
                )
            
            return HttpResponse(status=201)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)