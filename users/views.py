from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import login, logout

from .serializers import UserCreateSerializer, LoginSerializer, UserSerializer
from .models import User


from rest_framework import generics, response, permissions, authentication


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class CsrfExemptSessionAuthentication(authentication.SessionAuthentication):
    def enforce_csrf(self, request):
        return


class LoginView(APIView):

    permission_classes = (permissions.AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return response.Response(UserSerializer(user).data)

    """
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
            raise AuthenticationFailed('Password is incorrect')

        response = Response()
        response.data = {
            'message': 'Successfully Logged In',
        }
        return response
    """


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response()
