import datetime
import os

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from django.db.models import QuerySet

from blog.models import Article, Category, Tag


class Command(BaseCommand):
    help = 'import articles'

    def add_arguments(self, parser):
        parser.add_argument('--dir', type=str, help='the dir of articles')

    def handle(self, *args, **options):
        import markdown
        md = markdown.Markdown(extensions=['meta'])
        path = options['dir'] if 'dir' in options else None
        User = get_user_model()
        author = User.objects.first()
        if path and os.path.exists(path):
            filenames = os.listdir(path)
            for filename in filenames:
                if filename.endswith('md'):
                    print(filename)
                    full_path = os.path.join(path, filename)
                    file = open(full_path, encoding='utf-8').read()
                    md.convert(file)
                    metas = md.Meta
                    body = file
                    if 'categories' in metas and metas['categories'][0]:
                        category_name = metas['categories'][0]
                    else:
                        category_name = '无分类'
                    category = Category.objects.filter(name=category_name).first()
                    if not category:
                        category = Category(name=category_name)
                        category.save()
                    article = Article(title=metas['title'][0], author=author, body=body, category=category)
                    if 'slug' in metas and metas['slug'][0]:
                        article.slug = metas['slug'][0]
                    if 'date' in metas and metas['date'][0]:
                        article.pub_time = metas['date'][0]
                    else:
                        article.pub_time = datetime.datetime.now()
                    if 'updated' in metas and metas['updated'][0]:
                        article.modify_time = metas['updated'][0]
                    else:
                        article.modify_time = article.pub_time
                    if 'tags' in metas and metas['tags']:
                        for tag_name in metas['tags']:
                            tag = Tag.objects.filter(name=tag_name).first()
                            if not tag:
                                tag = Tag(name=category_name)
                                tag.save()
                            article.tags.add(tag)
                    article.save()
