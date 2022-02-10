import json, re, bcrypt, jwt

from django.views           import View
from django.http            import JsonResponse, HttpResponse
from django.core.exceptions import ValidationError 
from django.conf            import settings

from .models                import User

class SignUpView(View):
    def post(self, request):
        try:
            user_data = json.loads(request.body)
            name            = user_data["name"]
            email           = user_data['email']
            password        = user_data['password']
            phone_number    = user_data["phone_number"]
            address         = user_data["address"]
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            REGEX_EMAIL    = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
            REGEX_PASSWORD = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'

            if name == '':
                return JsonResponse({"message" : "Please type your name"}, status = 400)
            
            if not re.fullmatch(REGEX_EMAIL, email):
                return JsonResponse({"message" : "Please type valid email address"}, status = 400)

            if not re.fullmatch(REGEX_PASSWORD, password):
                return JsonResponse({"message" : "must have 1 alphabet, 1 numbers, 1 special character and minimum 8 letter"}, status = 400)

            if User.objects.filter(email = email).exists():
                return JsonResponse({"message" : "email already exist"}, status = 400)

            user = User.objects.create(
                name         = name,
                email        = email,
                password     = hashed_password.decode('utf-8'),
                phone_number = phone_number,
                address      = address,
                point        = 1000000
            )
            return JsonResponse({"message" : "SUCCESS"}, status = 201)
        
        except KeyError as e:
            return JsonResponse({"message" : "KEY_ERROR: " + str(e).replace("'", '')}, status = 401)

class SignInView(View):
    def post(self, request):
        
        user_data = json.loads(request.body)

        try:
            email    = user_data['email']
            password = user_data['password']
            user     = User.objects.get(email = email)
            
            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({"message" : "wrong password"}, status = 400)

            access_token = jwt.encode({'user_id' : user.id}, settings.SECRET_KEY, settings.ALGORITHM)
            return JsonResponse({"message" : "LOGIN SUCCESS!", "Token" : access_token, "Name" : user.name}, status = 201)
        
        except KeyError as e:
            return JsonResponse({"message" : "KEY_ERROR: " + str(e).replace("'", '')}, status = 401)
        
        except User.DoesNotExist:
            return JsonResponse({"message" : "invaild email"}, status = 400)
        