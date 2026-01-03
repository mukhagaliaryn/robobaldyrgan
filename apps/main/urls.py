from django.urls import path
from .views import main, auth

app_name = 'main'

urlpatterns = [
    path('', main.home, name='home'),

    # auth views...
    path('login/', auth.login_view, name='login'),
    path('register/', auth.register_view, name='register'),
    path('logout/', auth.logout_view, name='logout'),
]
