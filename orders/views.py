from django.http  import HttpResponse
from django.views import View

from .models         import Cart

class CartView(View):
    def delete(self, request, product_option_id):
        Cart.objects.filter(
            user           = request.user.id,
            product_option = product_option_id
            ).delete()

        return HttpResponse(status=204)