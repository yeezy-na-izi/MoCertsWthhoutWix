from datetime import datetime

from django.conf import settings


from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import PasswordChangeView as ChangePasswordView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages

from django.core.mail import EmailMessage

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.http import HttpResponseNotFound, HttpResponseRedirect

from django.shortcuts import render, redirect

from django.urls import reverse_lazy, reverse

from django.views.generic import TemplateView

from .certificates.certificate_generator import generate_certificate
from main.forms import UserForm
from main.models import Account, Certificate
from main.utils import token_generator
from .names.names_generator import false_user


class MainView(TemplateView):
    template_name = 'index.html'


def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        user_form = UserForm(data=request.POST, files=request.FILES)
        if user_form.is_valid() and not Account.objects.get(email=request.POST['username']):
            user_form.is_active = False
            user = user_form.save()
            user.is_active = False
            user.save()

            user_id = urlsafe_base64_encode(force_bytes(user.email))
            domain = get_current_site(request).domain
            activate_url = f'http://{domain}/activate/{user_id}/{token_generator.make_token(user)}'

            email_subject = 'Подтверждение почты'
            email_body = f'Привет, {user}, это активация аккаунта, перейди по ссылке чтобы ' \
                         f'верефицировать свой аккаунт\n{activate_url}'
            email = EmailMessage(email_subject, email_body, 'noreply@semycolon.com', [user.email], )
            email.send(fail_silently=False)

            return redirect('/login')
        elif Account.objects.get(email=request.POST['email']):
            messages.error(request, 'Вы уже были зарегистрированы')
    else:
        user_form = UserForm()
    return render(request, 'index.html', {})


class MyCertsLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True


@login_required
def profile_view(request, pk):
    if request.user.pk == pk:
        context = {'object': request.user}
        return render(request, template_name='profile.html', context=context)
    return HttpResponseNotFound('<h1>Page not found</h1>')


class ManualView(TemplateView):
    template_name = 'manual.html'


class SelectCertificateView(TemplateView):
    template_name = 'select_certificate.html'


def verification_email(request, user_id, token):
    try:
        email = force_text(urlsafe_base64_decode(user_id))
        user = Account.objects.get(email=email)
        if token_generator.check_token(user, token) and not user.is_active:
            user.is_active = True
            user.save()
            return redirect('/login')
        return redirect('/login')
    except:
        pass
    return redirect('/login')


@login_required
def create_certificate(request, nominal):
    if request.method == 'GET':
        if request.user.certificate:
            return HttpResponseRedirect(reverse('certificate',
                                                kwargs={'number': request.user.certificate.number}))
        number = datetime.today().strftime("%d%m%y%H%M%f")
        url = '{}/certificate/{}'.format(settings.HOST, number)
        user1_fullname = false_user()
        user2_fullname = false_user()
        user3_fullname = false_user()
        user1 = Account(first_name=user1_fullname[0],
                        last_name=user1_fullname[1],
                        email=f'fakeuser1{number}.gmail.com',
                        password=user2_fullname)
        user2 = Account(first_name=user2_fullname[0],
                        last_name=user2_fullname[1],
                        email=f'fakeuser2{number}.gmail.com',
                        password=user3_fullname)
        user3 = Account(first_name=user3_fullname[0],
                        last_name=user3_fullname[1],
                        email=f'fakeuser3{number}.gmail.com',
                        password=user1_fullname)
        user1.save()
        user2.save()
        user3.save()
        image_certificate = generate_certificate(nominal, number, user1, user2, user3)
        certificate = Certificate(number=number, url=url, nominal=nominal,
                                  user1=user1, user2=user2, user3=user3, certificate_image=image_certificate)
        certificate.save()
        mycertuser = request.user
        mycertuser.certificate = certificate
        mycertuser.save()
        return HttpResponseRedirect(reverse('certificate',
                                            kwargs={'number': request.user.certificate.number}))


@login_required
def certificate(request, number):
    mycertuser = request.user
    certificate = mycertuser.certificate
    if certificate and number == mycertuser.certificate.number:
        context = {'certificate': certificate, 'transfer': True}
        return render(request, template_name='certificate.html', context=context)
    certificate = Certificate.objects.get(number=number)
    if certificate.made_by == mycertuser:
        context = {'certificate': certificate}
        return render(request, template_name='certificate.html', context=context)
    if certificate.status != 'NONE':
        context = {'certificate': certificate}
        return render(request, template_name='certificate.html', context=context)
    context = {'certificate': certificate, 'accept': True}
    return render(request, template_name='certificate.html', context=context)


@login_required
def accept(request, pk):
    certificate = Certificate.objects.get(pk=pk)
    certificate.status = 'RECEIVED'
    certificate.save()
    request.user.certificate = certificate
    request.user.save()
    return HttpResponseRedirect(reverse('certificate',
                                        kwargs={'number': certificate.number}))


@login_required
def pay_certificate(request, pk):
    if request.user.certificate.pk == pk:
        certificate = request.user.certificate
        if request.user.balance >= certificate.nominal:
            request.user.balance -= certificate.nominal
            certificate.payed = True
            certificate.status = 'PAID'
            certificate.save()
            request.user.certificate = None
            for i in range(0, 5):
                certificate.user1.balance += certificate.nominal
                user1, user2, user3 = certificate.user2, certificate.user3, request.user
                number = datetime.today().strftime("%d%m%y%H%M%f")
                image_certificate = generate_certificate(certificate.nominal, number, user1, user2, user3)
                url = '{}/certificate/{}'.format(settings.HOST, number)
                new_certificate = Certificate(number=number, url=url, nominal=certificate.nominal,
                                              user1=user1, user2=user2, user3=user3,
                                              certificate_image=image_certificate)
                new_certificate.made_by = request.user
                new_certificate.save()
            request.user.save()
            return HttpResponseRedirect(reverse('my_certificates'))
        else:
            return HttpResponseRedirect(reverse('certificate', kwargs={'number': certificate.number}))
    return HttpResponseNotFound('<h1>Page not found</h1>')


@login_required
def my_certificates(request):
    certificates = Certificate.objects.filter(made_by=request.user)
    context = {'certificates_1': [],
               'certificates_5': [],
               'certificates_10': [],
               'certificates_20': [],
               'certificates_50': [],
               'certificates_100': [],
               'certificates_200': [],
               'certificates_500': []}
    for cert in certificates:
        if cert.nominal == 1:
            context['certificates_1'].append(cert)
        elif cert.nominal == 5:
            context['certificates_5'].append(cert)
        elif cert.nominal == 10:
            context['certificates_10'].append(cert)
        elif cert.nominal == 20:
            context['certificates_20'].append(cert)
        elif cert.nominal == 50:
            context['certificates_50'].append(cert)
        elif cert.nominal == 100:
            context['certificates_100'].append(cert)
        elif cert.nominal == 200:
            context['certificates_200'].append(cert)
        elif cert.nominal == 500:
            context['certificates_500'].append(cert)
    return render(request, template_name='my_certificates.html', context=context)


class PasswordsChangeView(ChangePasswordView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('main_page')
