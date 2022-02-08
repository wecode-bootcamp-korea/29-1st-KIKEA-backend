import json

from django.views import View
from django.http  import JsonResponse, HttpResponse

from users.models import User
from users.utils  import login_decorator
from .models      import *


class ReviewView(View):
    @login_decorator
    def post(self, request):
        try:
            review_data = json.loads(request.body)
            comment     = review_data['comment']
            rating      = review_data['rating']
            product_id  = review_data['product_id']
            user_id     = request.user.id

            review, is_review = Review.objects.get_or_create(
                comment    = comment,
                rating     = rating,
                product_id = product_id,
                user_id    = user_id
            )
            if not is_review:
                return JsonResponse({"message" : "review already exist"}, status = 201)
            return JsonResponse({"message" : "SUCCESS"}, status = 201)
        
        except KeyError as e:
            return JsonResponse({"message" : "KEY_ERROR: " + str(e).replace("'", '')}, status = 400)


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