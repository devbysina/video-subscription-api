from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.throttling import UserRateThrottle

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .serializers import RegisterSerializer, MeSerializer, ChangePasswordSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['post']
    throttle_classes = [UserRateThrottle]

class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = MeSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'patch']

    def get_object(self):
        return self.request.user

class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        user = request.user
        ser = self.get_serializer(data=request.data, context={'request': request})
        ser.is_valid(raise_exception=True)

        old_password = ser.validated_data['old_password']
        new_password = ser.validated_data['new_password']

        if not check_password(old_password, user.password):
            raise ValidationError({"old_password": "Old password is incorrect."})

        user.set_password(new_password)
        user.save(update_fields=['password'])
        return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        refresh = request.data.get('refresh')
        if not refresh:
            return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh)
            token.blacklist()
        except TokenError:
            return Response({"detail": "Invalid or expired refresh token."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Logged out."}, status=status.HTTP_200_OK)
