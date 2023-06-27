from django.contrib import admin
from .models import Genre, Filmwork, GenreFilmwork, Person, PersonFilmwork


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (PersonFilmworkInline,
               GenreFilmworkInline,
               )

    # Отображение полей в списке
    list_display = ('title', 'type', 'creation_date', 'show_rating',)

    # Фильтрация в списке
    list_filter = ('type', 'creation_date')

    # Поиск по полям
    search_fields = ('title', 'description', 'id')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass
