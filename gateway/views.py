from re import L
import jwt
from .models import Jwt
from authentication.models import CustomUser

from datetime import datetime, timedelta
from django.conf import settings
import random, string
from rest_framework.views import APIView
from .serializers import LoginSerializer

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

        access = get_access_token({"user_id":user.id})
        refresh = get_refresh_token()

        Jwt.objects.create(
            user_id = user.id,
            acess_token = access,
            refresh_token = refresh
        )

        return Response({"access":access,"refresh":refresh})
