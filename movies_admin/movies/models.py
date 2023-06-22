import uuid

from django.db import models


class Genre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    g_name = models.CharField('g_name', max_length=35)
    description = models.TextField('description', blank=True)
    # auto_now_add выставит дату СОЗДАНИЯ записи автоматически
    created = models.DateTimeField(auto_now_add=True)
    # auto_now выставит дату ИЗМЕНЕНИЯ записи
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


