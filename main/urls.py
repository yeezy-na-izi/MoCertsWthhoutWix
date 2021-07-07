from django.contrib.auth.views import LogoutView
from django.urls import path
from main.views import MainView, profile_view, MyCertsLoginView, register, ManualView, \
    SelectCertificateView, create_certificate, certificate, pay_certificate, accept, my_certificates, \
    verification_email, PasswordsChangeView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', MainView.as_view(), name='main_page'),

    path('login', MyCertsLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='main_page'), name='logout'),
    path('profile/<int:pk>/', profile_view, name='profile'),
    path('registration', register, name='registration'),
    path('activate/<user_id>/<token>', verification_email, name='activate'),

    path('manual', ManualView.as_view(), name='manual'),

    path('select_certificate', SelectCertificateView.as_view(), name='select_certificate'),
    path('create_certificate/<int:nominal>/', create_certificate, name='create_certificate'),
    path('certificate/<int:number>/', certificate, name='certificate'),
    path('my_certificates', my_certificates, name='my_certificates'),
    path('pay_certificate/<int:pk>', pay_certificate, name='pay_certificate'),
    path('accept/<int:pk>', accept, name='accept'),

    path('change_password', PasswordsChangeView.as_view(template_name='change_password.html'), name='changepassword'),
    path('reset_password',
         auth_views.PasswordResetView.as_view(template_name='password/password_reset.html'),
         name='reset_password'),
    path('reset_password_sent',
         auth_views.PasswordResetDoneView.as_view(template_name='password/reset_password_sent.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name='password/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset_password_complete',
         auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'),
         name='password_reset_complete'),

]
