from re import L
import jwt
from .models import Jwt
from authentication.models import CustomUser

from datetime import datetime, timedelta
from django.conf import settings
import random, string
from rest_framework.views import APIView
from .serializers import LoginSerializer, RegisterSerializer, RefreshSerializer

from django.contrib.auth import authenticate

from rest_framework.response import Response

def get_random(length):
    return ''.join(random.choices(string.ascii_uppercase+string.digits,k=length))

def get_access_token(payload):
    return jwt.encode(
        {"exp": datetime.now()+timedelta(minutes=5), **payload},
        settings.SECRET_KEY,
        algorithm="HS256"
    )

def get_refresh_token():
    return jwt.encode(
        {"exp": datetime.now()+timedelta(days=265), "data":get_random(10)},
        settings.SECRET_KEY,
        algorithm="HS256"
    )

class LoginView(APIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(username=serializer.validated_data['email'],password=serializer.validated_data['password'])

        if not user:
            return Response({"Error!":"Invalid email or password"},status="400")

        Jwt.objects.filter(user_id=user.id).delete()
        access = get_access_token({"user_id":user.id})
        refresh = get_refresh_token()


        Jwt.objects.create(
            user_id = user.id,
            acess_token = access,
            refresh_token = refresh
        )

        return Response({"access":access,"refresh":refresh})


class RegisterView(APIView):
    serializer_class = RegisterSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        CustomUser.objects._create_user(**serializer.validated_data)

        return Response({"msg":"User created."})

def verify_token(token):
    #decode the token
    try:
        decoded_data = jwt.decode(token,settings.SECRET_KEY, algorithms="HS256")
        print("First try passed")
    except Exception as e:
        print(e)
        return None
    #check if token has expired
    exp = decoded_data["exp"]
    if datetime.now().timestamp() > exp:
        return None
    else:
        return decoded_data


class RefreshView(APIView):
    serializer_class = RefreshSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            active_jwt = Jwt.objects.get(refresh_token=serializer.validated_data["refresh_token"])
        except Jwt.DoesNotExist:
            return Response({"error":"refresh token not found."},status="400")

        if not verify_token(serializer.validated_data["refresh_token"]):
            return Response({"error":"Token is invalid or has expired"})

        else:
            access = get_access_token({"user_id":active_jwt.user.id})
            refresh = get_refresh_token()

            active_jwt.access_token = access
            active_jwt.refresh_token = refresh
            active_jwt.save()

            return Response({"access":access, "refresh":refresh})