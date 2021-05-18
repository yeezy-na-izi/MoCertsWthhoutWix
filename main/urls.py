from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from main.views import MainView, profile_view, RegisterFormView, MyCertsLoginView, register, ManualView

app_name = 'main'
urlpatterns = [
    path('', MainView.as_view(), name='main_page'),
    path('login', MyCertsLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='main:main_page'), name='logout'),
    path('profile/<int:pk>/', profile_view, name='profile'),
    path('registration', register, name='registration'),
    path('manual', ManualView.as_view(), name='manual'),
]