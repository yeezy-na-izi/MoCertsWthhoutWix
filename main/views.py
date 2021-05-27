from datetime import datetime

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, FormView
from .certificates.certificate_generator import generate_certificate

from main.forms import UserForm, MyCertUserForm
from main.models import MyCertsUser, Certificate

from .names.names_generator import false_user


class MainView(TemplateView):
    template_name = 'main.html'


def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        mycertuser_form = MyCertUserForm(data=request.POST, files=request.FILES)
        if user_form.is_valid() and mycertuser_form.is_valid():
            new_user = user_form.save()
            new_mycertuser = MyCertsUser.objects.create(user=new_user)
            profile_photo = mycertuser_form.cleaned_data.get("profile_photo")
            new_mycertuser.profile_photo = profile_photo
            new_mycertuser.save()
            authenticate(request, username=new_user.username, password=new_user.password)
            login(request, new_user)
            return HttpResponseRedirect(reverse('main:main_page'))
    else:
        user_form = UserForm()
        mycertuser_form = MyCertUserForm()
    return render(request, 'registration.html', {
        'user_form': user_form,
        'mycertuser_form': mycertuser_form
    })


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


@login_required
def create_certificate(request, nominal):
    if request.method == 'GET':
        if request.user.mycertsuser.certificate:
            return HttpResponseRedirect(reverse('main:certificate',
                                                kwargs={'number': request.user.mycertsuser.certificate.number}))
        number = datetime.today().strftime("%d%m%y%H%M%f")
        url = '{}/certificate/{}'.format(settings.HOST, number)
        user1_fullname = false_user()
        user2_fullname = false_user()
        user3_fullname = false_user()
        user1 = User(username='FAKEUSER1_{}'.format(number),
                     first_name=user1_fullname[0],
                     last_name=user1_fullname[1])
        user2 = User(username='FAKEUSER2_{}'.format(number),
                     first_name=user2_fullname[0],
                     last_name=user2_fullname[1])
        user3 = User(username='FAKEUSER3_{}'.format(number),
                     first_name=user3_fullname[0],
                     last_name=user3_fullname[1])
        user1.save()
        user2.save()
        user3.save()
        image_certificate = generate_certificate(nominal, number, user1, user2, user3)
        certificate = Certificate(number=number, url=url, nominal=nominal,
                                  user1=user1, user2=user2, user3=user3, certificate_image=image_certificate)
        certificate.save()
        mycertuser = request.user.mycertsuser
        mycertuser.certificate = certificate
        mycertuser.save()
        return HttpResponseRedirect(reverse('main:certificate',
                                            kwargs={'number': request.user.mycertsuser.certificate.number}))


@login_required
def certificate(request, number):
    mycertuser = request.user.mycertsuser
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
    request.user.mycertsuser.certificate = certificate
    request.user.mycertsuser.save()
    return HttpResponseRedirect(reverse('main:certificate',
                                        kwargs={'number': certificate.number}))


@login_required
def pay_certificate(request, pk):
    if request.user.mycertsuser.certificate.pk == pk:
        certificate = request.user.mycertsuser.certificate
        if request.user.mycertsuser.balance >= certificate.nominal:
            request.user.mycertsuser.balance -= certificate.nominal
            certificate.payed = True
            certificate.status = 'PAID'
            certificate.save()
            request.user.mycertsuser.certificate = None
            for i in range(0, 5):
                user1, user2, user3 = certificate.user2, certificate.user3, request.user
                number = datetime.today().strftime("%d%m%y%H%M%f")
                image_certificate = generate_certificate(certificate.nominal, number, user1, user2, user3)
                url = '{}/certificate/{}'.format(settings.HOST, number)
                new_certificate = Certificate(number=number, url=url, nominal=certificate.nominal,
                                              user1=user1, user2=user2, user3=user3,
                                              certificate_image=image_certificate)
                new_certificate.made_by = request.user.mycertsuser
                new_certificate.save()
            request.user.mycertsuser.save()
            return HttpResponseRedirect(reverse('main:my_certificates'))
        else:
            return HttpResponseRedirect(reverse('main:certificate', kwargs={'number': certificate.number}))
    return HttpResponseNotFound('<h1>Page not found</h1>')


@login_required
def my_certificates(request):
    certificates = Certificate.objects.filter(made_by=request.user.mycertsuser)
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
