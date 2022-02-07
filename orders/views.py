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