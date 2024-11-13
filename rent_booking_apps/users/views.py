from rest_framework import views, viewsets, mixins
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from rent_booking_apps.users.serializers import *


class RegisterView(GenericAPIView):
    serializer_class = RegisterSerializer


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer


class LogoutView(views.APIView):
    permission_classes = None


class ProtectedView(views.APIView):
    def get(self, request, *args, **kwargs):
        #  GET-запрос
        return Response({'message': 'GET запрос выполнен'})

    def post(self, request, *args, **kwargs):
        #  POST-запрос
        return Response({'message': 'POST запрос выполнен'})


class UserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def my_profile(self, request):
        queryset = User.objects.get(pk=request.user.pk)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)
