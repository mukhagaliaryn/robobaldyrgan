from django.contrib import admin
from core.admin._mixins import LinkedAdminMixin
from django.utils.translation import gettext_lazy as _
from core.forms.course import CourseAdminForm, LessonAdminForm
from core.models import Course, Chapter, Lesson


# Course admin
# ----------------------------------------------------------------------------------------------------------------------
class ChapterInline(LinkedAdminMixin, admin.TabularInline):
    model = Chapter
    extra = 0
    readonly_fields = ('detail_link',)

    def detail_link(self, obj):
        return self.admin_link(obj, label=_('Толығырақ'))
    detail_link.short_description = _('Сілтеме')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at', 'last_update', 'access', 'view', )
    list_filter = ('owner', 'access', )
    search_fields = ('name', )

    form = CourseAdminForm
    inlines = (ChapterInline, )


# Chapter admin
# ----------------------------------------------------------------------------------------------------------------------
class LessonInline(LinkedAdminMixin, admin.TabularInline):
    model = Lesson
    fields = ('order', 'title', 'course', 'detail_link', )
    extra = 0
    readonly_fields = ('detail_link',)

    def detail_link(self, obj):
        return self.admin_link(obj, label=_('Толығырақ'))
    detail_link.short_description = _('Сілтеме')


@admin.register(Chapter)
class ChapterAdmin(LinkedAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'course', 'order', )
    list_filter = ('course', )
    search_fields = ('name', )
    readonly_fields = ('course_link', )

    def course_link(self, obj):
        return self.parent_link(obj, 'course')

    course_link.short_description = _('Курс')
    inlines = (LessonInline, )


# Lesson
# ----------------------------------------------------------------------------------------------------------------------
@admin.register(Lesson)
class LessonAdmin(LinkedAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'chapter', 'created_at', 'last_update', 'order', )
    list_filter = ('course', 'chapter', )
    search_fields = ('title', )
    readonly_fields = ('chapter_link', )
    form = LessonAdminForm

    def chapter_link(self, obj):
        return self.parent_link(obj, 'chapter')

    chapter_link.short_description = _('Модуль')
