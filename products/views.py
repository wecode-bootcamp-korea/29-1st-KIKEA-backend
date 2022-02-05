from django.views           import View
from django.http            import JsonResponse, HttpResponse

from .models                import *

class CategoryView(View):
    def get(self, request):
        categories = Category.objects.all()

        results = [{
            "id" : category.id,
            "name" : category.name,
            "subcategory_list" : [{
                "id" : subcategory.id,
                "name" : subcategory.name,
                "type_list" : [{
                    "id" : type.id,
                    "name" : type.name,
                    "product_list" : [{
                        "id" : product.id,
                        "name" : product.name,
                        "description" : product.description,
                        "default_image" : product.default_image,
                    } for product in type.product_set.all()]
                } for type in subcategory.type_set.all()]                    
            } for subcategory in category.subcategory_set.all()]
        } for category in categories]

        return JsonResponse({"categories" : results}, status = 200)
        
