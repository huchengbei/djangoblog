from abc import abstractmethod

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
    article = models.ForeignKey(Article, verbose_name='文章', on_delete=models.PROTECT)
    parent = models.ForeignKey('self', verbose_name='父评论', blank=True, null=True, on_delete=models.SET_NULL)
    username = models.CharField(verbose_name='名字', max_length=20)
    email = models.EmailField(verbose_name='邮箱')
    website = models.URLField(verbose_name='网站')
    content = models.TextField(verbose_name='内容')

    class Meta:
        ordering = ['-create_time']

    def get_absolute_url(self):
        return self.article.get_absolute_url() + '#comment-' + str(self.id)
