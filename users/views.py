from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

import datetime
import jwt

from .serializers import UserSerializer, UserCreateSerializer
from .models import User


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
            raise AuthenticationFailed('Password is incorrect')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.now() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.now(),
        }

        token = jwt.encode(payload, 'secret',
                           algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'message': 'Successfully Logged In',
        }
        return response


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        user = User.objects.get(id=payload['id'])
        user_serialized = UserSerializer(user)
        return (Response(user_serialized.data))


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Successfully Logged Out',
        }
        return response
