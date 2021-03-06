from abc import abstractmethod

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from mdeditor.fields import MDTextField

from slugify import slugify

# Create your models here.


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        abstract = True

    @abstractmethod
    def get_absolute_url(self):
        pass


class Article(BaseModel):
    STATUS = (
        ('draft', '草稿'),
        ('published', '发表'),
    )
    COMMENT_STATUS = (
        ('open', '打开'),
        ('close', '关闭'),
    )
    TYPE = (
        ('article', '文章'),
        ('page', '页面'),
    )

    title = models.CharField('标题', max_length=50)
    slug = models.SlugField('Slug', max_length=50, unique=True, blank=True, help_text='显示在URL中的标识')
    type = models.CharField('类型', max_length=7, choices=TYPE, default='article')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='作者', on_delete=models.PROTECT)
    pub_time = models.DateTimeField('发布时间', blank=True)
    modify_time = models.DateTimeField('更改时间', blank=True)
    summary = models.TextField('摘要', max_length=200, blank=True, help_text='文章摘要置空默认提取文字内容前部分文字')
    body = MDTextField('正文', help_text='支持markdown')
    comment_type = models.CharField('评论状态', max_length=5, choices=COMMENT_STATUS, default='open')
    views = models.PositiveIntegerField('浏览量', default=0)
    loves = models.PositiveIntegerField('喜爱量', default=0)
    category = models.ForeignKey('Category', verbose_name='分类', on_delete=models.PROTECT)
    tags = models.ManyToManyField('Tag', blank=True, verbose_name='标签')

    image_link = models.CharField('图片地址', blank=True, max_length=255, help_text='用于封面的图片地址')

    status = models.CharField('发表状态', max_length=9, choices=STATUS, default='published')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-pub_time']
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        get_latest_by = 'id'

    def get_absolute_url(self):
        url_pattern = 'blog:article' if self.type == 'article' else 'blog:page'
        return reverse(url_pattern, kwargs={
            'slug': self.slug,
        })

    def get_category_breadcrumb(self):
        breads = self.category.get_ancestor_category_list()
        breadcrumb = list(map(lambda c: (c.name, c.get_absolute_url()), breads))
        return breadcrumb

    def get_summary(self):
        import markdown
        md = markdown.Markdown(extensions=['meta'])
        md.convert(self.body)
        lines = md.lines
        from functools import reduce
        body = reduce(lambda x, y: x + '\n' + y, lines)
        return body[0:150]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[0:50]
        if not self.summary:
            self.summary = self.get_summary()
        super().save(*args, **kwargs)

    def viewed(self):
        self.views += 1
        self.save(update_fields=['views'])

    def loved(self):
        self.loves += 1
        self.save(update_fields=['loves'])

    def get_admin_url(self):
        url_pattern = 'admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name)
        return reverse(url_pattern, args=(self.id,))

    def has_pre(self):
        pre_article = Article.objects.filter(pub_time__lt=self.pub_time, status='published', type=self.type)\
            .order_by('-pub_time').first()
        return True if pre_article else False

    def has_next(self):
        next_article = Article.objects.filter(pub_time__gt=self.pub_time, status='published', type=self.type)\
            .order_by('pub_time').first()
        return True if next_article else False

    def get_pre(self):
        return Article.objects.filter(pub_time__lt=self.pub_time, status='published', type=self.type)\
            .order_by('-pub_time').first()

    def get_next(self):
        return Article.objects.filter(pub_time__gt=self.pub_time, status='published', type=self.type)\
            .order_by('pub_time').first()


class Category(BaseModel):
    name = models.CharField('分类名', max_length=30, unique=True)
    slug = models.SlugField('Slug', max_length=50, unique=True, blank=True, help_text='显示在URL中的标识')
    parent = models.ForeignKey('self', verbose_name='父分类', blank=True, null=True, on_delete=models.PROTECT)
    description = models.TextField('描述', max_length=240, blank=True, help_text='SEO中description')

    class Meta:
        ordering = ['id']
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category', kwargs={
            'slug': self.slug
        })

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_ancestor_category_list(self):
        category = self
        category_list = [category, ]
        while category.parent:
            category = category.parent
            category_list.append(category)

        return category_list[::-1]

    def get_child_category_dict(self):
        def make_dict(dic):
            for k, v in dic.items():
                sub_category_list = Category.objects.filter(parent=k)
                for c in sub_category_list:
                    dic[k][c] = {}
            for k, v in dic.items():
                make_dict(dic[k])

        dic = {
            self: {}
        }

        make_dict(dic)
        return dic


class Tag(BaseModel):
    name = models.CharField('标签名', max_length=30, unique=True)
    slug = models.SlugField('Slug', max_length=50, unique=True, blank=True, help_text='显示在URL中的标识')
    description = models.TextField('描述', max_length=240, blank=True, help_text='SEO中description')

    class Meta:
        ordering = ['id']
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:tag', kwargs={
            'slug': self.slug
        })


class Navigation(BaseModel):
    TYPE = (
        ('category', '分类'),
        ('page', '页面'),
        ('article', '文章'),
        ('link', '链接'),
        ('blank', '空'),
    )

    name = models.CharField('导航名', max_length=30, blank=True, help_text='置空则为相应实体名字')
    icon = models.CharField('图标', max_length=30, blank=True, null=True,
                            help_text='fontawesome图标名, class内名称，如 "fa fa-home" ')
    type = models.CharField('导航类型', max_length=8, choices=TYPE, default='blank')
    parent = models.ForeignKey('self', verbose_name='父导航', blank=True, null=True, on_delete=models.SET_NULL)
    instance_id = models.IntegerField('实体id', blank=True, null=True)
    sequence = models.IntegerField('排序', default=0)
    is_show = models.BooleanField('是否展示', default=True)

    class Meta:
        ordering = ['sequence', 'id']
        verbose_name = '导航栏'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.name:
            if self.type == 'category':
                self.name = Category.objects.filter(id=self.instance_id).first().name
            if self.type == 'article' or self.type == 'page':
                self.name = Article.objects.filter(id=self.instance_id).first().title
            if self.type == 'link':
                self.name = FriendLink.objects.filter(id=self.instance_id).first().name
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        if self.type == 'category':
            return Category.objects.filter(id=self.instance_id).first().get_absolute_url()
        if self.type == 'article' or self.type == 'page':
            return Article.objects.filter(id=self.instance_id).first().get_absolute_url()
        if self.type == 'link':
            return Link.objects.filter(id=self.instance_id).first().get_absolute_url()
        return '#'


class Link(BaseModel):
    name = models.CharField('网站名', max_length=30, unique=True)
    url = models.CharField('链接地址', max_length=200)
    logo = models.URLField('网址Logo', blank=True)

    class Meta:
        verbose_name = '链接'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return str(self.url)


class FriendLink(Link):
    sequence = models.IntegerField('排序', unique=True)
    is_show = models.BooleanField('是否展示', default=True)

    class Meta:
        ordering = ['sequence']
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name


class ExtendsSideBar(models.Model):
    """
    sidebar, show some html content
    """
    name = models.CharField('网站名', max_length=30, unique=True)
    content = models.TextField('HTML内容')
    sequence = models.IntegerField('排序', unique=True)
    is_show = models.BooleanField('是否展示', default=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        ordering = ['sequence']
        verbose_name = '拓展侧边栏'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class BlogSetting(models.Model):
    site_name = models.CharField('网站名称', max_length=200, default='')
    site_url = models.URLField('网站地址')
    site_description = models.CharField('网站描述', max_length=1000, default='')
    site_seo_description = models.CharField('网站SEO描述', max_length=1000, blank=True)
    site_keywords = models.CharField('网站关键字', max_length=1000, default='')

    open_ads = models.BooleanField('启用广告', default=False)
    open_comment = models.BooleanField('启用评论', help_text='在网站中启用评论功能', default=False)

    sidebar_article_num = models.IntegerField('侧边栏文章数目', default=10)
    sidebar_comment_num = models.IntegerField('侧边栏评论数目', default=10)
    paginate_by = models.IntegerField('每页展示文章数', default=10)

    ads_content_codes = models.TextField('广告代码', max_length=2000, blank=True, default='', help_text='广告HTML代码')

    ICP_number = models.CharField('备案号', max_length=100, blank=True, default='')
    analytics_code = models.TextField('网站统计代码', max_length=1000, blank=True, default='')
    show_gongan_number = models.BooleanField('是否显示备案号', default=False)
    gongan_number = models.CharField('公安备案号', max_length=100, blank=True, default='')
    static_source = models.CharField('静态文件地址', max_length=200, blank=True, default='')

    class Meta:
        verbose_name = '网站配置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.site_name

    def clean(self):
        if BlogSetting.objects.exclude(id=self.id).count():
            raise ValidationError(_('只能存在一个配置'))

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    @staticmethod
    def get_settings():
        return BlogSetting.objects.first()

    @staticmethod
    def get_site_url():
        return BlogSetting.objects.first().site_url
