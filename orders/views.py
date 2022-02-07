from django.http  import HttpResponse, JsonResponse
from django.views import View

from .models         import Cart
from users.models    import User
from users.utils     import @login_decorator
from products.models import ProductOption

class CartView(View):
    @login_decorator
    def post(self, request, product_option_id):
        try:
            quantity = 1
            
            cart, created = Cart.objects.get_or_create(
                    product_option = ProductOption.objects.get(id=product_option_id),
                    user           = User.objects.get(id=request.user.id),
                    defaults       = {'quantity':1}
                    )

            if not created:
                cart.quantity += quantity
                cart.save()
                return HttpResponse(status=204)
                
            return HttpResponse(status=201)
        except ProductOption.DoesNotExist:
            return JsonResponse({'message': 'INVALID_PRODUCT_OPTION'}, status=400)