from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title, Users


class UserSelfRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ('email', 'username')

    def username_validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                'Нельзя создать пользователя с именем me')
        return data


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('id', )


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id', )


class TitlesSerializerGet(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(
        source='ratings.ratings', read_only=True
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name',
            'year', 'category',
            'genre', 'description', 'rating'
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    title = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    class Meta:
        model = Review
        fields = '__all__'

    def validate(self, data):
        if Review.objects.filter(
                title=self.context['view'].kwargs['title_id'],
                author=self.context['request'].user
        ).exists() and self.context['request'].method == 'POST':
            raise serializers.ValidationError(
                'Нельзя оставить два отзыва на одно произведение')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'pub_date')


class TitlesSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )
    rating = serializers.IntegerField(
        source='ratings.ratings', read_only=True
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name',
            'year', 'category',
            'genre', 'description', 'rating'
        )


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        read_only_fields = (
            'username',
            'email',
            'role'
        )


class UsersForAdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
