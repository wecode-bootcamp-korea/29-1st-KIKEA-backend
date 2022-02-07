import json

from django.http  import HttpResponse
from django.views import View

from .models import Cart

class CartView(View):
    @login_decorator
    def patch(self, request, product_option_id):
        data     = json.loads(request.body)
        quantity = data['quantity']

        cart = Cart.objects.filter(user=request.user, product_option=product_option_id)

        if quantity == '0':
            cart.delete()
            return HttpResponse(status=204)

        cart.update(quantity=quantity)

        return HttpResponse(status=200)