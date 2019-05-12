from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.utils.http import is_safe_url
from django.views.generic import ListView, DetailView, FormView, RedirectView

from account.forms import UserCreationForm, LoginForm
from account.models import User


class RegisterView(FormView):
    form_class = UserCreationForm
    template_name = 'account/re.html'

    def form_valid(self, form):
        user = form.save(False)
        user.save()
        url = reverse('account:login')
        return HttpResponseRedirect(url)

    def get_context_data(self, **kwargs):
        to_url = self.request.GET.get('to_url')
        if not to_url:
            to_url = '/'

        kwargs['to_url'] = to_url
        return super(RegisterView, self).get_context_data(**kwargs)


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'account/lo.html'
    default_success_url = '/admin'

    def get_context_data(self, **kwargs):
        to_url = self.request.POST.get('to_url')
        if not to_url:
            to_url = self.request.GET.get('to_url')
        if not to_url:
            to_url = '/'
        kwargs['to_url'] = to_url
        return super(LoginView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        form = AuthenticationForm(data=self.request.POST, request=self.request)

        print(2)
        if form.is_valid():
            auth.login(self.request, form.get_user())
            return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        to_url = self.request.POST.get('to_url')
        # if not is_safe_url(url=to_url, allowed_hosts=[self.request.get_host()]):
        #     to_url = self.default_success_url
        return to_url



