from django import forms

from blog.models import Navigation, Category, Article, Link


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'

    def clean(self):
        cleaned_data = super(ArticleForm, self).clean()
        if self.has_changed():
            changed_data = self.changed_data
            if 'title' in changed_data or 'author' in changed_data or \
                    'summary' in changed_data or 'body' in changed_data:
                from django.utils import timezone
                cleaned_data['modify_time'] = timezone.now()
        return cleaned_data


class NavigationForm(forms.ModelForm):
    category_id = forms.ChoiceField(label='分类', help_text='请导航类型选择分类时选择此项')
    page_id = forms.ChoiceField(label='页面', help_text='请导航类型选择页面时选择此项')
    article_id = forms.ChoiceField(label='文章', help_text='请导航类型选择文章时选择此项')
    link_id = forms.ChoiceField(label='链接', help_text='请导航类型选择链接时选择此项')
    field_order = ['name','icon', 'type', 'parent', 'instance_id', 'category_id', 'page_id', 'article_id', 'link_id',
                   'sequence', 'is_show']

    class Meta:
        model = Navigation
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category_id'].choices = \
            ((0, '请选择分类'),) + tuple(Category.objects.all().values_list('id', 'name'))
        self.fields['page_id'].choices = \
            ((0, '请选择页面'),) + tuple(Article.objects.filter(type='page').values_list('id', 'title'))
        self.fields['article_id'].choices = \
            ((0, '请选择文章'),) + tuple(Article.objects.filter(type='article').values_list('id', 'title'))
        self.fields['link_id'].choices = \
            ((0, '请选择链接'),) + tuple(Link.objects.all().values_list('id', 'name'))
        self.fields['instance_id'].widget = forms.HiddenInput()
        if 'type' in self.initial and self.initial['type'] != 'blank':
            if 'instance_id' in self.initial and self.initial['instance_id']:
                self.fields[self.initial['type'] + '_id'].initial = self.initial['instance_id']

    def clean(self):
        cleaned_data = super(NavigationForm, self).clean()
        type = cleaned_data.get('type')
        category_id = int(cleaned_data.get('category_id'))
        page_id = int(cleaned_data.get('page_id'))
        article_id = int(cleaned_data.get('article_id'))
        link_id = int(cleaned_data.get('link_id'))
        if type == 'category':
            if category_id is 0:
                msg = '请选择分类'
                self.add_error('category_id', msg)
        if type == 'page':
            if page_id is 0:
                msg = '请选择页面'
                self.add_error('page_id', msg)
        if type == 'article':
            if article_id is 0:
                msg = '请选择文章'
                self.add_error('article_id', msg)
        if type == 'link':
            if link_id is 0:
                msg = '请选择链接'
                self.add_error('link_id', msg)
        if type == 'blank':
            name = cleaned_data.get('name')
            if not name:
                msg = '导航类型为空时需设置导航名'
                self.add_error('name', msg)

        if type != 'blank':
            cleaned_data['instance_id'] = cleaned_data[type + '_id']
        return cleaned_data
