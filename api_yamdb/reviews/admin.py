from django.contrib import admin

from .models import (Category, Comment, Genre, GenreTitle, Rating, Review,
                     Title, Users)


class UsersAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'username',
                    'email',
                    'role',
                    'bio',
                    'first_name',
                    'last_name',
                    'confirmation_code')
    search_fields = ('username', 'email')
    empty_value_display = '-пусто-'


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'year',
        'category',
        'description',
    )
    search_fields = (
        'name',
        'year',
        'category'
    )
    empty_value_display = '-пусто-'


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name', 'slug')
    list_display = (
        'id',
        'name',
        'slug'
    )
    search_fields = ('name', 'slug')
    empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug'
    )
    search_fields = ('name', 'slug')
    empty_value_display = '-пусто-'


class GenreTitleAdmin(admin.ModelAdmin):
    list_display = ('genre', 'title')


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'text',
        'author',
        'score',
        'pub_date'
    )
    search_fields = (
        'title',
        'author',
        'score',
        'pub_date'
    )
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'review',
        'text',
        'author',
        'pub_date',
    )
    search_fields = (
        'author',
        'pub_date'
    )
    empty_value_display = '-пусто-'


class RatingAdmin(admin.ModelAdmin):
    list_display = (
        'title_id',
        'ratings',
    )


admin.site.register(Users, UsersAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(GenreTitle, GenreTitleAdmin)
