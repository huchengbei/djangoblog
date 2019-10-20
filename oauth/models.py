import uuid
from abc import abstractmethod

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from django.urls import reverse
from slugify import slugify

from blog.models import BlogSetting


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        abstract = True


class UserEx(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='用户', on_delete=models.PROTECT)
    openid = models.CharField(verbose_name='OpenId', max_length=100)
    platform = models.ForeignKey('Platform', verbose_name='认证平台', on_delete=models.PROTECT)

    class Meta:
        verbose_name = '授权表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.user)


class Platform(BaseModel):
    PLATFORM_CHOICE = (
        ('github', 'Github'),
        ('weibo', '微博'),
        ('wechat', '微信'),
        ('qq', 'QQ'),
    )

    name = models.CharField('平台名', max_length=10, choices=PLATFORM_CHOICE)
    slug = models.SlugField('Slug', max_length=50, unique=True, blank=True)
    icon = models.CharField('图标', max_length=30, blank=True,
                            help_text='fontawesome图标名, class内名称，如 "fab fa-github" ')
    client_id = models.CharField('Client ID', max_length=100)
    client_secret = models.CharField('Client Secret', max_length=100)
    auth_url = models.URLField('认证网址', blank=True, null=True, help_text='不填则使用默认认证网址')
    token_url = models.URLField('获取令牌网址', blank=True, null=True, help_text='不填则使用默认认证网址')

    callback_url = models.URLField('回调地址', blank=True, null=True, help_text='定制回调地址，默认空')

    sequence = models.IntegerField('排序', default=0)
    is_show = models.BooleanField('是否展示', default=True)

    plat_entity = None

    class Meta:
        ordering = ['sequence']
        verbose_name = '认证平台'
        verbose_name_plural = verbose_name

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.plat_entity = self.get_plat_entity()

    def __str__(self):
        return dict(self.PLATFORM_CHOICE)[self.name]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[0:50]
        super().save(*args, **kwargs)

    def get_plat_entity(self):
        if self.name == 'github':
            return Github(self.client_id, self.client_secret, self.auth_url, self.token_url)
        if self.name == 'weibo':
            return Weibo(self.client_id, self.client_secret, self.auth_url, self.token_url)
        if self.name == 'wechat':
            return Wechat(self.client_id, self.client_secret, self.auth_url, self.token_url)
        if self.name == 'qq':
            return QQ(self.client_id, self.client_secret, self.auth_url, self.token_url)
        return None

    def get_auth_url(self):
        return self.plat_entity.get_auth_url()

    def get_callback_url(self):
        return self.callback_url if self.callback_url else BlogSetting.get_site_url() + reverse('oauth:callback')

    def get_token(self, code):
        return self.plat_entity.get_token(code) if self.plat_entity else None

    def get_auth_user(self, access_token):
        return self.plat_entity.get_user(access_token=access_token) if self.plat_entity else None

    def get_or_create_user(self, access_token):
        user_info = self.get_auth_user(access_token)
        platform = Platform.objects.get(name=user_info['platform'])
        user_ex = UserEx.objects.filter(platform=platform, openid=user_info['openid']).first()
        UserModel = get_user_model()
        if user_ex:
            return UserModel.objects.get(id=user_ex.user.id)

        user = UserModel()
        if user.username and user.username != user_info['username']:
            while UserModel.objects.filter(username=user_info['username']):
                import random
                user_info['username'] += str(random.randint(10, 99))
            user.username = user_info['username']
        pwd = str(uuid.uuid1())  # 随机设置用户密码
        user.set_password(pwd)
        user.email = user_info['email']
        if 'nickname' in dir(UserModel):
            user.nickname = user_info['nickname']
        if 'link' in dir(UserModel):
            user.link = user_info['link']
        if 'avatar' in dir(UserModel):
            user.avatar = user_info['avatar']
        user.save()

        user_ex = UserEx()
        user_ex.platform = platform
        user_ex.openid = user_info['openid']
        user_ex.user = user
        user_ex.save()
        return user


class BaseOAuthPlat:
    client_id = None
    client_secret = None
    auth_url = None
    token_url = None

    class Meta:
        abstract = True

    @abstractmethod
    def get_auth_url(self, **kwargs):
        pass

    @abstractmethod
    def get_token(self, code, **kwargs):
        pass

    @abstractmethod
    def get_user(self, access_token, **kwargs):
        pass

    @abstractmethod
    def format_user_info(self, user, **kwargs):
        pass


class Github(BaseOAuthPlat):
    auth_url = 'https://github.com/login/oauth/authorize'
    token_url = 'https://github.com/login/oauth/access_token'
    user_url = 'https://api.github.com/user'

    def __init__(self, client_id, client_secret, auth_url=None, token_url=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_url = auth_url or self.auth_url
        self.token_url = token_url or self.token_url

    def get_auth_url(self, **kwargs):
        return "{auth_url}?client_id={client_id}".format(auth_url=self.auth_url, client_id=self.client_id)

    def get_token(self, code, **kwargs):
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
        }
        header = {
            'accept': 'application/json'
        }
        res = requests.post(self.token_url, headers=header, data=params)
        if res.status_code == 200:
            res_dict = res.json()
            if 'access_token' in res_dict.keys():
                return res_dict['access_token']
        return None

    def get_user(self, access_token, **kwargs):
        user_url = self.user_url
        access_token = 'token {}'.format(access_token)
        headers = {
            'accept': 'application/json',
            'Authorization': access_token
        }
        res = requests.get(user_url, headers=headers)
        if res.status_code == 200:
            res_dict = res.json()
            return self.format_user_info(res_dict)
        return None

    def format_user_info(self, user, **kwargs):
        info = {}
        if 'login' not in user.keys():
            return None
        info['username'] = user['login']
        info['nickname'] = user['name']
        info['openid'] = user['node_id']
        info['avatar'] = user['avatar_url']
        info['link'] = user['blog']
        info['email'] = user['email']
        info['bio'] = user['bio']
        info['platform'] = 'github'
        return info


class Weibo(BaseOAuthPlat):
    auth_url = 'https://api.weibo.com/oauth2/authorize'
    token_url = 'https://api.weibo.com/oauth2/access_token'
    user_url = 'https://api.weibo.com/2/users/show.json'
    uid = None

    def __init__(self, client_id, client_secret, auth_url=None, token_url=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_url = auth_url or self.auth_url
        self.token_url = token_url or self.token_url

    def get_auth_url(self, **kwargs):
        return "{auth_url}?client_id={client_id}".format(auth_url=self.auth_url, client_id=self.client_id)

    def get_token(self, code, **kwargs):
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': BlogSetting.get_site_url() + reverse('oauth:callback'),
        }
        header = {
            'accept': 'application/json'
        }
        res = requests.post(self.token_url, headers=header, data=params)
        if res.status_code == 200:
            res_dict = res.json()
            if 'access_token' in res_dict.keys():
                self.uid = res_dict['uid']
                return res_dict['access_token']
        return None

    def get_user(self, access_token, **kwargs):
        params = {
            'access_token': access_token,
            'uid': self.uid,
        }
        res = requests.get(self.user_url, params=params)
        if res.status_code == 200:
            res_dict = res.json()
            return self.format_user_info(res_dict)
        return None

    def format_user_info(self, user, **kwargs):
        info = {}
        if 'error' in user.keys():
            return None
        info['username'] = user['idstr']
        info['nickname'] = user['screen_name']
        info['openid'] = self.uid
        info['avatar'] = user['profile_image_url']
        info['link'] = user['profile_url']
        info['platform'] = 'weibo'
        return info


class Wechat(BaseOAuthPlat):
    auth_url = 'https://open.weixin.qq.com/connect/qrconnect'
    token_url = 'https://api.weixin.qq.com/sns/oauth2/access_token'
    user_url = 'https://api.weixin.qq.com/sns/userinfo'
    openid=None

    def __init__(self, client_id, client_secret, auth_url=None, token_url=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_url = auth_url or self.auth_url
        self.token_url = token_url or self.token_url

    def get_auth_url(self, **kwargs):
        return "{auth_url}?appid={appid}&response_type={response_type}&state={state}&scope={scope}" \
            .format(auth_url=self.auth_url, appid=self.client_id, response_type='code', state='login',
                    scope='snsapi_login')

    def get_token(self, code, **kwargs):
        params = {
            'appid': self.client_id,
            'secret': self.client_secret,
            'code': code,
            'grant_type': 'authorization_code',
        }
        header = {
            'accept': 'application/json'
        }
        res = requests.post(self.token_url, headers=header, data=params)
        if res.status_code == 200:
            res_dict = res.json()
            if 'access_token' in res_dict.keys():
                self.openid = res_dict['openid']
                return res_dict['access_token']
        return None

    def get_user(self, access_token, **kwargs):
        params = {
            'access_token': access_token,
            'openid': self.openid,
        }
        res = requests.get(self.user_url, params=params)
        if res.status_code == 200:
            res_dict = res.json()
            return self.format_user_info(res_dict)

    def format_user_info(self, user, **kwargs):
        info = {}
        if 'error' in user.keys():
            return None
        info['username'] = 'wechat_' + str(uuid.uuid1())[0:10]
        info['nickname'] = user['nickname']
        info['openid'] = user['unionid']
        info['avatar'] = user['headimgurl']
        info['platform'] = 'wechat'
        return info


class QQ(BaseOAuthPlat):
    auth_url = 'https://graph.qq.com/oauth2.0/authorize'
    token_url = 'https://graph.qq.com/oauth2.0/token'
    openid_url = 'https://graph.qq.com/oauth2.0/me'
    user_info_url = 'https://graph.qq.com/user/get_user_info'

    def __init__(self, client_id, client_secret, auth_url=None, token_url=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_url = auth_url or self.auth_url
        self.token_url = token_url or self.token_url

    def get_auth_url(self, **kwargs):
        return "{auth_url}?response_type={response_type}&client_id={client_id}&state={state}&scope={scope}" \
            .format(auth_url=self.auth_url, response_type='code', client_id=self.client_id, state='login',
                    scope='get_user_info')

    def get_token(self, code, **kwargs):
        params = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'redirect_uri': BlogSetting.get_site_url() + reverse('oauth:callback'),
        }
        header = {
            'accept': 'application/json'
        }
        res = requests.get(self.token_url, headers=header, params=params)
        if res.status_code == 200:
            res_dict = res.json()
            if 'access_token' in res_dict.keys():
                return res_dict['access_token']
        return None

    def get_user(self, access_token, **kwargs):
        params = {
            'access_token': access_token,
        }
        header = {
            'accept': 'application/json'
        }
        res = requests.get(self.openid_url, headers=header, params=params)
        openid = None
        if res.status_code == 200:
            res_dict = res.json()
            if 'openid' in res_dict.keys():
                openid = res_dict['openid']
        if not openid:
            return None
        params = {
            'access_token': access_token,
            'oauth_consumer_key': self.client_id,
            'openid': openid,
        }
        header = {
            'accept': 'application/json'
        }
        res = requests.get(self.user_info_url, headers=header, params=params)
        if res.status_code == 200:
            res_dict = res.json()
            res_dict['openid'] = openid
            return self.format_user_info(res_dict)
        return None

    def format_user_info(self, user, **kwargs):
        info = {}
        if user['ret'] != 0:
            return None
        info['username'] = 'qq_' + str(uuid.uuid1())[0:10]
        info['nickname'] = user['nickname']
        info['openid'] = user['openid']
        info['avatar'] = user['figureurl_1']
        info['platform'] = 'qq'
        return info
