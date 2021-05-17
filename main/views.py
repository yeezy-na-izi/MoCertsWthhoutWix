from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, FormView

from main.forms import UserForm, MyCertUserForm
from main.models import MyCertsUser


class MainView(TemplateView):
    template_name = 'main.html'


class RegisterFormView(FormView):
    form_class = UserForm
    success_url = '/'
    template_name = "registration.html"

    def form_valid(self, form):
        user = form.save()
        mycertsuser = MyCertsUser(user=user)
        mycertsuser.save()
        return super(RegisterFormView, self).form_valid(form)

    def form_invalid(self, form):
        return super(RegisterFormView, self).form_invalid(form)


def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        mycertuser_form = MyCertUserForm(data=request.POST, files=request.FILES)
        if user_form.is_valid() and mycertuser_form.is_valid():
            new_user = user_form.save()
            new_mycertuser = MyCertsUser.objects.create(user=new_user)
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
