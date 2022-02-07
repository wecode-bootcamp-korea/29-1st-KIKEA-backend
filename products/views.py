from django.views           import View
from django.http            import JsonResponse, HttpResponse

from .models                import *

class TypeView(View):
    def get(self, request):
        types = Type.objects.filter(subcategory__name__in = request.GET.getlist('subcategory'))

        results = [{
            "id"        : type.id,
            "name"      : type.name,
            "image_url" : type.image_url,
        } for type in types]

        return JsonResponse({"categories" : results}, status = 200)
        
