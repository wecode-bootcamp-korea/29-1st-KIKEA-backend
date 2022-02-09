from django.views           import View
from django.http            import JsonResponse, HttpResponse

from .models                import *

class TypeView(View):
    def get(self, request):
        types = Type.objects.filter(sub_category__id__in = request.GET.getlist('subcategory'))

        results = [{
            "id"        : type.id,
            "name"      : type.name,
            "image_url" : type.image_url,
        } for type in types]

        return JsonResponse({"types" : results}, status = 200)
        
class CategoryView(View):
    def get(self, request):
        categories = Category.objects.all()

        results = [{
            "id"               : category.id,
            "name"             : category.name,
            "subcategory_list" : [{
                "id"           : subcategory.id,
                "name"         : subcategory.name,                                 
            } for subcategory in category.subcategory_set.all()]
        } for category in categories]

        return JsonResponse({"categories" : results}, status = 200)
