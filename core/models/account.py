from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


# User model
# ----------------------------------------------------------------------------------------------------------------------
def avatar_upload_to(instance, filename):
    return f'avatars/users/{instance.id}/{filename}'


class User(AbstractUser):
    class Role(models.TextChoices):
        LEARNER = 'learner', _('Оқушы')
        TEACHER = 'teacher', _('Оқытушы')
        ADMIN = 'admin', _('Администрация')

    avatar = models.ImageField(_('Сурет'), upload_to=avatar_upload_to, blank=True, null=True)
    user_role = models.CharField(
        _('Қолданушы рөлі'),
        max_length=32,
        choices=Role.choices,
        default=Role.LEARNER,
        db_index=True,
    )

    def __str__(self):
        full = f"{self.first_name} {self.last_name}".strip()
        return full or self.username or self.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    class Meta:
        verbose_name = _('Қолданушы')
        verbose_name_plural = _('Қолданушылар')
