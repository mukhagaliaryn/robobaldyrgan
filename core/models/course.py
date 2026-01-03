from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import User


# Course model
# ----------------------------------------------------------------------------------------------------------------------
class Course(models.Model):
    class Access(models.TextChoices):
        PRIVATE = 'private', _('Жабық')
        PUBLIC = 'public', _('Ашық')

    name = models.CharField(_('Атауы'), max_length=128)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses', verbose_name=_('Авторы'))
    poster = models.ImageField(_('Постер'), blank=True, null=True, upload_to='core/course/posters')
    description = models.TextField(_('Анықтамасы'), blank=True, null=True)
    created_at = models.DateTimeField(_('Жасалған уақыты'), auto_now_add=True)
    last_update = models.DateTimeField(_('Соңғы өзгеріс'), auto_now=True)
    access = models.CharField(_('Қолжетімділік'), choices=Access.choices, default=Access.PRIVATE, max_length=32)
    view = models.PositiveIntegerField(_('Қаралым'), default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Курс')
        verbose_name_plural = _('Курстар')
        ordering = ('created_at', )


# Chapter model
# ----------------------------------------------------------------------------------------------------------------------
class Chapter(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE,
        verbose_name=_('Курс'), related_name='chapters'
    )
    name = models.CharField(_('Атауы'), max_length=128)
    order = models.PositiveIntegerField(_('Реттілік нөмері'), default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Модуль')
        verbose_name_plural = _('Модульдер')
        ordering = ('order', )


# Lesson model
# ----------------------------------------------------------------------------------------------------------------------
class Lesson(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE,
        verbose_name=_('Курс'), related_name='lessons', null=True, blank=True
    )
    chapter = models.ForeignKey(
        Chapter, on_delete=models.CASCADE,
        verbose_name=_('Модуль'), related_name='lessons'
    )
    title = models.CharField(_('Тақырыбы'), max_length=128)
    description = models.TextField(_('Анықтамасы'), blank=True, null=True)
    created_at = models.DateTimeField(_('Жасалған уақыты'), auto_now_add=True)
    last_update = models.DateTimeField(_('Соңғы өзгеріс'), auto_now=True)
    order = models.PositiveIntegerField(_('Реттілік нөмері'), default=0)

    def __str__(self):
        return self.title[:64]

    class Meta:
        verbose_name = _('Сабақ')
        verbose_name_plural = _('Сабақтар')
        ordering = ('order', )


# LessonDoc model
# ----------------------------------------------------------------------------------------------------------------------
class LessonDocs(models.Model):
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE,
        verbose_name=_('Сабақ'), related_name='docs'
    )
    title = models.CharField(_('Тақырыбы'), max_length=255)
    file = models.FileField(_('Файл'), upload_to='core/lesson/docs/', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Сабақ құжаты')
        verbose_name_plural = _('Сабақ құжаттары')
