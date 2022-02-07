import json

from django.http  import HttpResponse
from django.views import View

from .models         import Cart
from users.utils     import login_decorator

class CartView(View):
    @login_decorator
    def delete(self, request, product_option_id):
        Cart.objects.filter(
            user           = request.user,
            product_option = product_option_id
            ).delete()

        return HttpResponse(status=204)

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
