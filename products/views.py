from django.views           import View
from django.http            import JsonResponse, HttpResponse
from django.db.models       import Q, Avg, Count

from .models                import *

class ProductOptionView(View):
    def get(self, request):
        try:
            category_name    = request.GET.getlist('category', None)
            subcategory_name = request.GET.getlist('subcategory', None)
            type_name        = request.GET.getlist('type', None)
            product_name     = request.GET.getlist('product')
            sorting          = request.GET.get('sort', '-created_at')

            q = Q()

            if category_name:
                q &= Q(product__type__sub_category__category__id__in = category_name)
            
            if subcategory_name:
                q &= Q(product__type__sub_category__id__in = subcategory_name)

            if type_name:
                q &= Q(product__type__id__in = type_name)
            
            if product_name:
                q &= Q(product__id__in = product_name)
            
            productoptions = ProductOption.objects.filter(q).order_by(sorting).prefetch_related('product__review_set')

            result = [{
                "id"            : productoption.id,
                "price"         : productoption.price,
                "stock"         : productoption.stock,
                "color"         : productoption.color.name if productoption.color else None,
                "size"          : productoption.size.name if productoption.size else None,
                "product_id"    : productoption.product_id,
                "default_image" : productoption.product.default_image,
                "description"   : productoption.product.description,
                "type"          : productoption.product.type.name,
                "name"          : productoption.product.name,
                "review_rating" : productoption.product.review_set.aggregate(rating=Avg('rating'))['rating'],
                "review_count"  : productoption.product.review_set.aggregate(count =Count('rating'))['count'],  
                "image"         : [image_url.image_url for image_url in productoption.productoptionimage_set.all()]
            }for productoption in productoptions]

            return JsonResponse({'message':'SUCCESS' ,'result' : result}, status=200)
        except Exception as e:
            return JsonResponse({'message': type(e)}, status=400)

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

class ProductOptionView(View):
    def get(self, request):
        try:
            category_name    = request.GET.getlist('category', None)
            subcategory_name = request.GET.getlist('subcategory', None)
            type_name        = request.GET.getlist('type', None)
            product_name     = request.GET.getlist('product', None)
            print(category_name)
            sorting          = request.GET.get('sort', 'id')
            #sort = request.GET.get('sort', '-id'
            # product_id = request.GET.get('product_id')
            # page       = request.GET.get('page',1)
            # page_size  = request.GET.get('page_size',5)


            q = Q()

            if category_name:
                q &= Q(product__type__sub_category__category__id__in = category_name)
            
            if subcategory_name:
                q &= Q(product__type__sub_category__id__in = subcategory_name)

            if type_name:
                q &= Q(product__type__id__in = type_name)
            
            if product_name:
                q &= Q(product__id__in = product_name)
            #"review_rating" : productoptions.aggregate(rating_average = Avg('product__review__rating').filter(product_id = productoption.product.review_set)),
                #"review_count"  : Review.objects.filter(product_id = productoption.product_id).aggregate(rating_count   = Count('rating')),
            #productoptions = ProductOption.objects.filter(q).order_by(sort)
            productoptions = ProductOption.objects.filter(q).order_by(sorting).prefetch_related('product__review_set')
            print(q)
            print(category_name)
            print(productoptions)
            result = [{
                "id"            : productoption.id,
                "price"         : productoption.price,
                "stock"         : productoption.stock,
                "color"         : productoption.color.name if productoption.color else None,
                "size"          : productoption.size.name if productoption.size else None,
                "product_id"    : productoption.product_id,
                "default_image" : productoption.product.default_image,
                "description"   : productoption.product.description,
                "type"          : productoption.product.type.name,
                "name"          : productoption.product.name,
                #"review_rating" : productoptions[0].product.review_set.aggregate(rating_average = Avg('rating')),
                # "review_rating" : productoptions.aggregate(rating_average = Avg('product__review__rating')),
                          
                "image"         : [image_url.image_url for image_url in productoption.productoptionimage_set.all()]
            }for productoption in productoptions]
            

               # productoption.product.review_set.all().aggregate(Avg('review'))

            return JsonResponse({'message':'SUCCESS' ,'result' : result}, status=200)
            
        except TypeError as e:
            return JsonResponse({'message': str(e)}, status=400)

        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)