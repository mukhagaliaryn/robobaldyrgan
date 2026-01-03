from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q
from core.models import Course
from django.utils import timezone


# dashboard page
# ----------------------------------------------------------------------------------------------------------------------
def dashboard_view(request):
    return render(request, 'app/platform/page.html', {})


# courses page
# ----------------------------------------------------------------------------------------------------------------------
def courses_view(request):
    q = (request.GET.get('q') or '').strip()

    courses_qs = (
        Course.objects
        .select_related('owner')
        .annotate(
            chapters_count=Count('chapters', distinct=True),
            lessons_count=Count('lessons', distinct=True),
        )
        .filter(access='public')
        .order_by('-created_at')
    )

    if q:
        courses_qs = courses_qs.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q) |
            Q(owner__username__icontains=q) |
            Q(owner__first_name__icontains=q) |
            Q(owner__last_name__icontains=q)
        )

    paginator = Paginator(courses_qs, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'q': q,
        'page_obj': page_obj,
        'courses': page_obj.object_list,
    }
    return render(request, 'app/platform/courses/page.html', context)


# course page
# ----------------------------------------------------------------------------------------------------------------------
def course_view(request, pk: int):
    course = (
        Course.objects
        .select_related('owner')
        .prefetch_related('chapters__lessons')
        .annotate(
            chapters_count=Count('chapters', distinct=True),
            lessons_count=Count('lessons', distinct=True),
        )
        .get(pk=pk)
    )

    Course.objects.filter(pk=course.pk).update(view=course.view + 1)
    chapters = course.chapters.all().order_by('order')

    context = {
        'course': course,
        'chapters': chapters,
    }
    return render(request, 'app/platform/courses/course/page.html', context)


def books_view(request):
    return render(request, 'app/platform/books/page.html')