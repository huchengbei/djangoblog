from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

from django.urls import reverse
from django.views.generic import FormView, RedirectView, UpdateView

from account.forms import UserCreationForm, LoginForm, UserChangeForm, PasswordChangeForm
from account.models import User
from blog.models import BlogSetting


# Create your views here.


class RegisterView(FormView):
    form_class = UserCreationForm
    template_name = 'account/register.html'

    def form_valid(self, form):
        user = form.save(False)
        user.save()
        next = self.request.POST.get('next', self.request.GET.get('next', ''))
        next = next if next else BlogSetting.get_site_url()
        url = reverse('account:login') + '?next=' + next
        return HttpResponseRedirect(url)

    def get_context_data(self, **kwargs):
        next = self.request.POST.get('next', self.request.GET.get('next', ''))
        kwargs['next'] = next
        return super(RegisterView, self).get_context_data(**kwargs)


# class LoginView(django.contrib.auth.views.LoginView )
class LoginView(FormView):
    form_class = LoginForm
    template_name = 'account/login.html'
    default_success_url = BlogSetting.get_site_url()

    def get_context_data(self, **kwargs):
        next = self.request.POST.get('next', self.request.GET.get('next', ''))
        kwargs['next'] = next
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        # it will auto auto authenticate the user
        auth.login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        kwargs = self.get_context_data()
        next = kwargs['next']
        if not next:
            next = self.default_success_url
        return next


class ChangeView(LoginRequiredMixin, UpdateView):
    form_class = UserChangeForm
    model = User
    template_name = 'account/change_profile.html'
    # do not login, just back to home
    login_url = BlogSetting.get_site_url()

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return self.request.GET.get('next', BlogSetting.get_site_url())

    def get_context_data(self, **kwargs):
        next = self.request.GET.get('next', BlogSetting.get_site_url())
        if 'next' not in kwargs:
            kwargs['next'] = next
        return super().get_context_data(**kwargs)


class PasswordChangeView(LoginRequiredMixin, UpdateView):
    form_class = PasswordChangeForm
    model = User
    template_name = 'account/change_password.html'
    # do not login, just back to home
    login_url = BlogSetting.get_site_url()

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return self.request.GET.get('next', BlogSetting.get_site_url())

    def get_context_data(self, **kwargs):
        next = self.request.GET.get('next', BlogSetting.get_site_url())
        if 'next' not in kwargs:
            kwargs['next'] = next
        return super().get_context_data(**kwargs)


class LogoutView(LoginRequiredMixin, RedirectView):
    # do not login, just back to home
    login_url = BlogSetting.get_site_url()

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        return super().get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        next = self.request.POST.get('next', self.request.GET.get('next', ""))
        self.url = next if next else BlogSetting.get_site_url()
        return self.url
