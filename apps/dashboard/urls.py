from django.urls import path
from .views import platform, account

app_name = 'platform'

urlpatterns = [
    path('', platform.dashboard_view, name='dashboard'),
    path('courses/', platform.courses_view, name='courses'),
    path('courses/<int:pk>/', platform.course_view, name='course'),
    path('books/', platform.books_view, name='books'),

    path('account/me/', account.account_view, name='account'),
    path('account/settings/', account.settings_view, name='settings'),
]