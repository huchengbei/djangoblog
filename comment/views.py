from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.views.generic import FormView

from blog.models import Article, BlogSetting
from comment.forms import CommentForm


class PostCommentView(FormView):
    form_class = CommentForm
    template_name = 'blog/article.html'

    def get(self, request, *args, **kwargs):
        article_id = request.GET['article']
        article = Article.objects.filter(id=article_id).first() if article_id else None
        if article:
            return HttpResponseRedirect(article.get_absolute_url())
        else:
            site = BlogSetting.get_site_url()
            url = "https://{site}".format(site=site)
            return HttpResponseRedirect(url)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, article=form.instance.article))

    def form_valid(self, form):
        comment = form.save(False)
        comment.save()
        return HttpResponseRedirect("{}#div-comment-{}".format(comment.article.get_absolute_url(), comment.id))
