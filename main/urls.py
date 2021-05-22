from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from main.views import MainView, profile_view, MyCertsLoginView, register, ManualView, \
    SelectCertificateView, create_certificate, certificate, pay_certificate, accept, my_certificates

app_name = 'main'
urlpatterns = [
    path('', MainView.as_view(), name='main_page'),
    path('login', MyCertsLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='main:main_page'), name='logout'),
    path('profile/<int:pk>/', profile_view, name='profile'),
    path('registration', register, name='registration'),
    path('manual', ManualView.as_view(), name='manual'),
    path('select_certificate', SelectCertificateView.as_view(), name='select_certificate'),
    path('create_certificate/<int:nominal>/', create_certificate, name='create_certificate'),
    path('certificate/<int:number>/', certificate, name='certificate'),
    path('pay_certificate/<int:pk>', pay_certificate, name='pay_certificate'),
    path('accept/<int:pk>', accept, name='accept'),
    path('my_certificates', my_certificates, name='my_certificates'),
]