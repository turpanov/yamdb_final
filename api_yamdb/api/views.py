from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import EmailValidator
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken


from .filter import TitleFilter
from .mixins import CreateListDestroyViewSet, CreateViewSet
from reviews.models import (Category, Comment, Genre, Rating, Review, Title,
                            Users)
from .permissions import AdminOrReadOnly, AuthorModerAdminOrReadOnly, IsAdmin
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitlesSerializer,
                          TitlesSerializerGet, UserSelfRegistrationSerializer,
                          UsersForAdminSerializer, UsersSerializer)
from .utils import (calculate_raiting, generate_confirmation_code,
                    send_confirmation_code)


class UserSelfRegistrationViewSet(CreateViewSet):
    """
    Класс для саморегистрации пользователя, пользователь отправляет на
    эндпойнт /users/signup/ - имя пользователя и эл. почту, и получает
    на почту код подтверждения для регистрации. Не возможна регистрация
    с именем me и ранее использованым именем пользователя и почтой. При
    отправке уже существующих имени пользователя и почты, будет выслан
    новый код.
    """
    serializer_class = UserSelfRegistrationSerializer
    permission_classes = [permissions.AllowAny, ]

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        EmailValidator(email)
        username = request.data.get('username')
        UnicodeUsernameValidator(username)

        if Users.objects.filter(email=email, username=username).exists():
            confirmation_code = generate_confirmation_code()
            Users.objects.filter(email=email, username=username).update(
                confirmation_code=confirmation_code)
            send_confirmation_code(confirmation_code, email)
            return Response(
                request.data,
                status=status.HTTP_200_OK,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = generate_confirmation_code()
        self.perform_create(serializer, confirmation_code)
        headers = self.get_success_headers(serializer.data)
        send_confirmation_code(confirmation_code, email)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            headers=headers
        )

    def perform_create(self, serializer, confirmation_code):
        serializer.save(confirmation_code=confirmation_code)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (AdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitlesSerializerGet
        return TitlesSerializer


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    pagination_class = LimitOffsetPagination
    lookup_field = 'slug'


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    pagination_class = LimitOffsetPagination
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = (AuthorModerAdminOrReadOnly, )
    queryset = Review.objects.all()

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title=title)
        avg_rating = calculate_raiting(title_id)
        Rating.objects.update_or_create(
            pk=title_id, defaults={'ratings': avg_rating})

    def perform_update(self, serializer):
        title_id = self.kwargs.get('title_id')
        serializer.save()
        avg_rating = calculate_raiting(title_id)
        Rating.objects.update_or_create(
            pk=title_id, defaults={'ratings': avg_rating})

    def perform_destroy(self, instance):
        title_id = self.kwargs.get('title_id')
        instance.delete()
        avg_rating = calculate_raiting(title_id)
        Rating.objects.update_or_create(
            pk=title_id, defaults={'ratings': avg_rating})


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AuthorModerAdminOrReadOnly,)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(author=self.request.user, review=review)


@api_view(['POST', ])
@permission_classes([permissions.AllowAny, ])
def user_get_token(request):
    """
    View предназначен для получения пользователем токена, после того как он
    получил код подтверждения. Пользователю необходимо отправить запрос с
    именем пользователя и кодом подтверждения на эндпойнт /users/token/. При
    правильном имени пользователя и коде система вернет токен, который
    необходимо указать для авторизации по методу Bearer
    """
    absent_fields = []
    if request.data.get('username') is None:
        absent_fields.append('username')
    if request.data.get('confirmation_code') is None:
        absent_fields.append('confirmation_code')
    if len(absent_fields) != 0:
        return Response(
            {'Absent_fields': absent_fields},
            status=status.HTTP_400_BAD_REQUEST
        )
    user = get_object_or_404(Users, username=request.data['username'])
    if user.confirmation_code == request.data['confirmation_code']:
        token = AccessToken.for_user(user=user)
        return Response({
            'token': str(token),
        }, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersForAdminSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdmin, )
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        detail=False,
        methods=('get', 'patch'),
        permission_classes=(permissions.IsAuthenticated, )
    )
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = UsersSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = UsersSerializer(
            user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
