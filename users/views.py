import json, re, bcrypt, jwt

from django.views           import View
from django.http            import JsonResponse, HttpResponse
from django.core.exceptions import ValidationError 

from .models                import User
from my_settings            import SECRET_KEY, ALGORITHM 

class SignUpView(View):
    def post(self, request):
        try:
            user_data       = json.loads(request.body)
            name            = user_data["name"]
            email           = user_data['email']
            password        = user_data['password']
            phone_number    = user_data["phone_number"]
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            REGEX_EMAIL     = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
            REGEX_PASSWORD  = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'

            if name == '':
                return JsonResponse({"message" : "Please type your name"}, status = 400)
            
            elif not re.fullmatch(REGEX_EMAIL, email):
                return JsonResponse({"message" : "Please type valid email address"}, status = 400)

            elif not re.fullmatch(REGEX_PASSWORD, password):
                return JsonResponse({"message" : "must have 1 alphabet, 1 numbers, 1 special character and minimum 8 letter"}, status = 400)

            elif User.objects.filter(email = email).exists():
                return JsonResponse({"message" : "email already exist"}, status = 400)

            else:
                user = User.objects.create(
                    name         = name,
                    email        = email,
                    password     = hashed_password.decode('utf-8'),
                    phone_number = phone_number
                )
                return JsonResponse({"message" : "SUCCESS"}, status = 201)
        
        except KeyError as e:
            return JsonResponse({"message" : "KEY_ERROR: " + str(e).replace("'", '')}, status = 401)
        
        except json.decoder.JSONDecodeError:
            return JsonResponse({"message" : "JSONDecodeError"}, status = 401)