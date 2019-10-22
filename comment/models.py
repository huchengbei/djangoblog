from abc import abstractmethod

from django.conf import settings
from django.db import models

# Create your models here.
from blog.models import Article


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        abstract = True

    @abstractmethod
    def get_absolute_url(self):
        pass


class Comment(BaseModel):

    STATUS = (
        ('open', '开发'),
        ('close', '屏蔽'),
    )
    article = models.ForeignKey(Article, verbose_name='文章', on_delete=models.PROTECT)
    parent = models.ForeignKey('self', verbose_name='父评论', blank=True, null=True, on_delete=models.SET_NULL)
    username = models.CharField(verbose_name='名字', max_length=20)
    email = models.EmailField(verbose_name='邮箱')
    website = models.URLField(verbose_name='网站', blank=True, null=True)
    content = models.TextField(verbose_name='内容')
    status = models.CharField('屏蔽状态', max_length=5, choices=STATUS, default='open')

    # if user login link here to user
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='所属用户', blank=True, null=True,
                             on_delete=models.PROTECT)

    class Meta:
        ordering = ['-create_time']
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return self.article.get_absolute_url() + '#comment-' + str(self.id)
