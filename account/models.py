from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    nickname = models.CharField('昵称', max_length=20, blank=True)
    link = models.URLField('个人网址', blank=True, help_text='请输入个人网址')
    avatar = models.URLField('头像', blank=True, help_text='请输入头像网址')
    email = models.EmailField('邮件地址', blank=True, null=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.nickname or self.get_username()


