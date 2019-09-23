from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect

# Create your views here.
from django.urls import reverse
from django.utils.http import is_safe_url
from django.views.generic import FormView, RedirectView

from account.forms import UserCreationForm, LoginForm
from blog.models import BlogSetting


class RegisterView(FormView):
    form_class = UserCreationForm
    template_name = 'account/register.html'

    def form_valid(self, form):
        user = form.save(False)
        user.save()
        to_url = self.request.POST.get('to_url', self.request.GET.get('to_url', ''))
        to_url = to_url if to_url else BlogSetting.get_site_url()
        url = reverse('account:login') + '?to_url=' + to_url
        return HttpResponseRedirect(url)

    def get_context_data(self, **kwargs):
        to_url = self.request.POST.get('to_url', self.request.GET.get('to_url', ''))
        kwargs['to_url'] = to_url
        return super(RegisterView, self).get_context_data(**kwargs)


# class LoginView(django.contrib.auth.views.LoginView )
class LoginView(FormView):
    form_class = LoginForm
    template_name = 'account/login.html'
    default_success_url = BlogSetting.get_site_url()

    def get_context_data(self, **kwargs):
        to_url = self.request.POST.get('to_url', self.request.GET.get('to_url', ''))
        kwargs['to_url'] = to_url
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        # it will auto auto authenticate the user
        auth.login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        kwargs = self.get_context_data()
        to_url = kwargs['to_url']
        if not to_url:
            to_url = self.default_success_url
        return to_url


class LogoutView(RedirectView):
    def get(self, request, *args, **kwargs):
        auth.logout(request)
        return super().get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        to_url = self.request.POST.get('to_url', self.request.GET.get('to_url', ""))
        self.url = to_url if to_url else BlogSetting.get_site_url()
        return self.url
