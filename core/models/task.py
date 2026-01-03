from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import Lesson


# Task model
# ----------------------------------------------------------------------------------------------------------------------
class Task(models.Model):
    TASK_TYPE = (
        ('video', _('Видеосабақ')),
        ('written', _('Жазбаша')),
        ('test', _('Тест')),
        ('matching', _('Сәйкестендіру')),
        # ('text_gap', _('Толықтыру')),
        # ('table', _('Кесте толтыру')),
    )

    PARAMS = (
        ('none', _('Таңдалмаған')),
        (_('Тест'), (
            ('quiz', _('Тест')),
            ('true-false', _('Ақиқат/жалған')),
        )),
        (_('Сәйкестендіру'), (
            ('row', _('Қатар')),
            ('col', _('Баған')),
        )),
    )

    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE,
        related_name='tasks', verbose_name=_('Сабақ')
    )
    task_type = models.CharField(_('Тапсырма түрі'), choices=TASK_TYPE, default='video', max_length=32)
    params = models.CharField(_('Параметрлер'), choices=PARAMS, default='none', max_length=32)
    rating = models.PositiveIntegerField(_('Жалпы бағасы'), default=0)
    duration = models.PositiveSmallIntegerField(_('Тапсырма уақыты (мин)'), default=0)
    description = models.TextField(_('Анықтамасы'), blank=True, null=True)
    order = models.PositiveIntegerField(_('Реттілік нөмері'), default=0)

    def __str__(self):
        return self.get_task_type_display()

    class Meta:
        verbose_name = _('Тапсырма')
        verbose_name_plural = _('Тапсырмалар')
        ordering = ('order', )


# Task type: Video model
# ----------------------------------------------------------------------------------------------------------------------
class Video(models.Model):
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, null=True,
        verbose_name=_('Контент'), related_name='videos'
    )
    url = models.TextField(_('Фрейм URL'))
    order = models.PositiveIntegerField(_('Реттілік нөмері'), default=0)

    def __str__(self):
        return _('#{} - видеосабақ').format(self.pk)

    class Meta:
        verbose_name = _('Видеосабақ')
        verbose_name_plural = _('Видеосабақтар')
        ordering = ('order', )


# Task type: Written model
# ----------------------------------------------------------------------------------------------------------------------
class Written(models.Model):
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE,
        related_name='writings', verbose_name=_('Тапсырма')
    )
    instruction = models.TextField(_('Тапсырма'), blank=True, null=True)

    def __str__(self):
        return _('#{} - жазбаша').format(self.pk)

    class Meta:
        verbose_name = _('Жазбаша')
        verbose_name_plural = _('Жазбашалар')


# Task type: Test model
# ----------------------------------------------------------------------------------------------------------------------
# Question model
class Question(models.Model):
    QUESTION_TYPE = (
        ('simple', _('Бір жауапты')),
        ('multiple', _('Көп жауапты')),
    )
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, null=True,
        related_name='questions', verbose_name=_('Тапсырма')
    )
    text = models.TextField(_('Сұрақ'))
    question_type = models.CharField(_('Сұрақтың түрі'), choices=QUESTION_TYPE, default='simple', max_length=32)
    order = models.PositiveIntegerField(_('Реттілік нөмері'), default=0)

    def __str__(self):
        return _('#{} - тест сұрағы').format(self.pk)

    class Meta:
        verbose_name = _('Тест сұрағы')
        verbose_name_plural = _('Тест сұрақтары')
        ordering = ('order', )


# Option model
class Option(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE,
        related_name='options', verbose_name=_('Сұрақ')
    )
    text = models.TextField(_('Жауап'), blank=True, null=True)
    is_correct = models.BooleanField(_('Дұрыс жауап'), default=False)

    def __str__(self):
        return _('#{} - нұсқа').format(self.pk)

    class Meta:
        verbose_name = _('Жауап')
        verbose_name_plural = _('Жауаптар')


# Task type: Matching model
# ----------------------------------------------------------------------------------------------------------------------
# MatchingColumn model
class MatchingColumn(models.Model):
    task = models.ForeignKey(
        Task, related_name='columns',
        on_delete=models.CASCADE, verbose_name=_('Тапсырма')
    )
    label = models.TextField(_('Атауы'))
    order = models.PositiveIntegerField(_('Реттілігі'), default=0)

    def __str__(self):
        return f'Сәйкес баған: {self.label} - бағаны'

    class Meta:
        verbose_name = _('Баған')
        verbose_name_plural = _('Бағандар')


# MatchingItem model
class MatchingItem(models.Model):
    correct_column = models.ForeignKey(
        MatchingColumn, related_name='correct_items',
        on_delete=models.CASCADE, verbose_name=_('Тапсырма')
    )
    text = models.TextField(_('Жауабы'), null=True, blank=True)

    def __str__(self):
        return self.text[:32]

    class Meta:
        verbose_name = _('Элемент')
        verbose_name_plural = _('Элементтер')


# Task type: TextGap model
# ----------------------------------------------------------------------------------------------------------------------
# class TextGap(models.Model):
#     task = models.ForeignKey(
#         Task, on_delete=models.CASCADE,
#         related_name='text_gaps', verbose_name=_('Сабақ')
#     )
#     prompt = models.TextField(_('Сөйлем (көп нүктемен)'))
#     correct_answer = models.CharField(_('Дұрыс жауап'), max_length=255)
#
#     def __str__(self):
#         return _('#{} - толықтыру').format(self.pk)
#
#     class Meta:
#         verbose_name = _('Толықтыру')
#         verbose_name_plural = _('Толықтырулар')