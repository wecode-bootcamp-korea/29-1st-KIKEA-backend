from django.http  import HttpResponse, JsonResponse
from django.views import View

from .models         import Cart
from users.models    import User
from products.models import ProductOption

class CartView(View):
    def post(self, request, product_option_id):
        try:
            quantity = 1

            user           = User.objects.get(id=request.user.id)
            product_option = ProductOption.objects.get(id=product_option_id)
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
        except ProductOption.DoesNotExist:
            return JsonResponse({'message': 'INVALID_PRODUCT_OPTION'}, status=400)