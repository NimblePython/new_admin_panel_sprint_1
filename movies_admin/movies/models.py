import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

from django.contrib import admin


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=35, default=_('not_define'))
    description = models.TextField(_('description'), blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('genre')
        verbose_name_plural = _('genres')


class Filmwork(UUIDMixin, TimeStampedMixin):
    title = models.CharField(_('title'), max_length=100)

    # Для форматированного вывода рейтинга на экран (напр. округленного)
    @admin.display(description=_('rating'))
    def show_rating(self):
        return self.rating

    description = models.TextField(_('description'), blank=True, null=True)
    creation_date = models.DateField(_('creation_date'), blank=True, null=True)
    # file_path = models.FilePathField(_('file_path'), blank=True, null=True)
    rating = models.FloatField(_('rating'),
                               blank=True,
                               null=True,
                               validators=[MinValueValidator(0),
                                           MaxValueValidator(100)]
                               )

    class FilmTypes(models.TextChoices):
        MOVIE = 'movie'
        TV_SHOW = 'tv_show'

    type = models.CharField(
        _('type'),
        max_length=35,
        choices=FilmTypes.choices,
        default=FilmTypes.MOVIE,
    )

    # Создание REFERENCES
    genres = models.ManyToManyField('Genre', through='GenreFilmwork', verbose_name=_('genres'))
    persons = models.ManyToManyField('Person', through='PersonFilmwork', verbose_name=_('persons'))

    def __str__(self):
        return self.title

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('movie')
        verbose_name_plural = _('movies')


class GenreFilmwork(UUIDMixin):
    # Создание REFERENCES
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)

    created_at = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        verbose_name = _('genre')
        verbose_name_plural = _('genres')
        constraints = [
            models.UniqueConstraint(fields=['film_work', 'genre'], name='unique_filmwork_genre'),
        ]


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_('full_name'), max_length=255)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('person')
        verbose_name_plural = _('persons')


class PersonFilmwork(UUIDMixin):
    # Создание REFERENCES
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)

    role = models.CharField(_('role'), max_length=35, null=True)
    created_at = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        verbose_name = _('person')
        verbose_name_plural = _('persons')
        constraints = [
            models.UniqueConstraint(fields=['film_work', 'person', 'role'], name='unique_filmwork_person_role'),
        ]
