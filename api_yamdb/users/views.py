from django.core.mail import send_mail
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import UserGetTokenSerializer, UserSignupSerializer


class UserSignupView(APIView):
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(data=serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        username = serializer.data['username']
        email = serializer.data['email']

        try:
            user, _ = User.objects.get_or_create(username=username,
                                                 email=email)
        except IntegrityError:
            return Response({'detail': 'Пользователь с таким'
                             ' username или email уже существует'},
                            status=status.HTTP_400_BAD_REQUEST)

        code = user.set_confirmation_code()

        send_mail('Код для доступа к API',
                  f'{code}',
                  'our@email.com',
                  [user.email],
                  fail_silently=True)

        return Response(data=serializer.data,
                        status=status.HTTP_200_OK)


class UserGetTokenView(APIView):
    def post(self, request):
        serializer = UserGetTokenSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(data=serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        username = serializer.data['username']
        code = serializer.data['confirmation_code']

        user = get_object_or_404(User, username=username)

        if user.confirmationcode.code == code:
            refresh = RefreshToken.for_user(user)
            return Response({'token': str(refresh.access_token)},
                            status=status.HTTP_200_OK)

        return Response(
            {'confirmation_code': 'Неправильный код подтверждения'},
            status=status.HTTP_400_BAD_REQUEST
        )
