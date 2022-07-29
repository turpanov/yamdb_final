from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, user_get_token,
                    UserSelfRegistrationViewSet, UsersViewSet)

router_v1_0 = routers.DefaultRouter()
router_v1_0.register(
    'auth/signup',
    UserSelfRegistrationViewSet,
    basename='auth'
)
router_v1_0.register('titles', TitleViewSet, basename='titles')
router_v1_0.register('categories', CategoryViewSet)
router_v1_0.register('genres', GenreViewSet)
router_v1_0.register(
    'users',
    UsersViewSet,
    basename='user-detail'
)
router_v1_0.register(
    r'titles/(?P<title_id>.+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1_0.register(
    r'titles/(?P<title_id>.+)/reviews/(?P<review_id>.+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router_v1_0.urls)),
    path('v1/auth/token/', user_get_token, name='token'),
]
