import json

from django.http  import HttpResponse, JsonResponse
from django.views import View

from .models         import Cart
from users.utils     import login_decorator
from products.models import ProductOption

class CartView(View):
    @login_decorator
    def post(self, request, product_option_id):
        data = json.loads(request.body)
        try:
            quantity = data['quantity']
            
            cart, created = Cart.objects.get_or_create(
                    product_option = ProductOption.objects.get(id=product_option_id),
                    user           = request.user,
                    defaults       = {'quantity': quantity}
                    )

            if not created:
                cart.quantity += quantity
                cart.save()
                return HttpResponse(status=204)
                
            return HttpResponse(status=201)
        except ProductOption.DoesNotExist:
            return JsonResponse({'message': 'INVALID_PRODUCT_OPTION'}, status=400)

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