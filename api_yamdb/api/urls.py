from django.urls import include, path
from rest_framework_nested import routers

from .views import (AdminUserViewSet, CategoryViewSet, CommentViewSet,
                    GenreViewSet, ReviewViewSet, TitleViewSet, UserMeView)

router = routers.DefaultRouter()

router.register('categories', CategoryViewSet, basename='сategories')
router.register('titles', TitleViewSet, basename='titles')
router.register('genres', GenreViewSet, basename='genres')
router.register('users', AdminUserViewSet, basename='users-admin')

titles_router = routers.NestedSimpleRouter(router, 'titles', lookup='title')
titles_router.register('reviews', ReviewViewSet, basename='title-reviews')

comment_router = routers.NestedSimpleRouter(titles_router, 'reviews',
                                            lookup='review')
comment_router.register('comments', CommentViewSet, basename='review-comments')


urlpatterns = [
    path('users/me/', UserMeView.as_view()),
    path('', include(router.urls)),
    path('', include(titles_router.urls)),
    path('', include(comment_router.urls))

]
