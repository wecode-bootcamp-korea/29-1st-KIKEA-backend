import json

from django.http  import HttpResponse
from django.views import View

from .models         import Cart
from users.models    import User

class CartView(View):
    def post(self, request, product_option_id):
        quantity = 1

        user = User.objects.get(id=request.user.id)
        cart = Cart.objects.filter(user=user.id, product_option=product_option_id)
        
        if cart.exists():
            quantity += cart[0].quantity
            cart.update(quantity=quantity)

            return HttpResponse(status=204)

        Cart.objects.create(
            quantity       = quantity,
            product_option = product_option_id,
            user           = user
            )
        
        return HttpResponse(status=201)