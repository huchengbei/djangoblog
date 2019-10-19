from django.contrib import auth
from django.http import HttpResponseRedirect

# Create your views here.

from oauth.models import Platform


def callback(request):
    code = request.GET.get('code', None)
    next = request.GET.get('next', None)
    slug = request.GET.get('slug', None)
    if not slug or not code:
        context = {
            'oauth_error_message': '授权失败',
            'next': next
        }
        from account.views import LoginView
        return LoginView.as_view(extra_context=context)(request)
    platform = Platform.objects.get(slug=slug)
    token = platform.get_token(code)
    if not token:
        context = {
            'oauth_error_message': '授权失败',
            'next': next
        }
        from account.views import LoginView
        return LoginView.as_view(extra_context=context)(request)
    user = platform.get_or_create_user(token)
    auth.login(request, user)
    return HttpResponseRedirect(next)

