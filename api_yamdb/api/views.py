from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api.filters import TitleFilter
from reviews.models import Review
from titles.models import Category, Genre, Title
from .mixins import CreateListDestroyMixin
from .permissions import IsAdmin, IsAuthor, IsModer, IsRead
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleReadSerializer, TitleWriteSerializer,
                          UserSerializer, UserWithoutRoleSerializer)

User = get_user_model()


class AdminUserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin, )
    lookup_field = 'username'
    search_fields = ('username', )
    filter_backends = (SearchFilter, )

    def update(self, request, *args, **kwargs):
        if kwargs.get('partial', False):
            return super().update(request, *args, **kwargs)

        return Response({'detail': 'PUT-запрос не предусмотрен'},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)


class UserMeView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = UserWithoutRoleSerializer(data=request.data,
                                               instance=request.user,
                                               partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(CreateListDestroyMixin):
    """Получить список всех категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (SearchFilter, )
    permission_classes = (IsAdmin | IsRead, )
    search_fields = ('name', )
    lookup_field = 'slug'


class GenreViewSet(CreateListDestroyMixin):
    """Получить список всех жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (SearchFilter, )
    permission_classes = (IsAdmin | IsRead, )
    search_fields = ('name', )
    lookup_field = 'slug'


class TitleViewSet(ModelViewSet):
    """Получить список всех произведений."""
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitleFilter
    permission_classes = (IsAdmin | IsRead, )

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(ModelViewSet):
    """Получение и изменение отзывов"""

    serializer_class = ReviewSerializer
    permission_classes = (IsAdmin | IsModer | IsAuthor | IsRead, )

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs['title_pk'])

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        try:
            serializer.save(author=self.request.user,
                            title=self.get_title())
        except IntegrityError:
            raise ValidationError({'detail': 'Обзор уже был сделан'})


class CommentViewSet(ModelViewSet):
    """Получение и отправка комментариев"""

    serializer_class = CommentSerializer
    permission_classes = (IsAdmin | IsModer | IsAuthor | IsRead, )

    def check_title(self):
        """Проверка, что произведение существует"""
        get_object_or_404(Title, pk=self.kwargs['title_pk'])

    def get_review(self):
        review = get_object_or_404(Review, pk=self.kwargs['review_pk'])
        return review

    def get_queryset(self):
        self.check_title()
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        self.check_title()
        serializer.save(author=self.request.user,
                        review=self.get_review())
