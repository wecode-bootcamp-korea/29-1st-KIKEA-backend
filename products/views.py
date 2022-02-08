from django.views           import View
from django.http            import JsonResponse, HttpResponse

from .models                import *

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
