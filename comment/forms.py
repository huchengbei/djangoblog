from django import forms

from comment.models import Comment


class CommentForm(forms.ModelForm):
    anti_spam = forms.CharField()

    class Meta:
        model = Comment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['anti_spam'].widget = forms.HiddenInput()
        self.fields['article'].widget = forms.HiddenInput()
        self.fields['parent'].widget = forms.HiddenInput()
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['username'].widget.attrs['placeholder'] = "名字"
        self.fields['email'].widget.attrs['placeholder'] = "邮箱"
        self.fields['website'].widget.attrs['placeholder'] = "网站"
        self.fields['content'].widget.attrs['placeholder'] = "一字千金"
        self.fields['content'].widget.attrs['rows'] = "5"

    def clean_anti_spam(self):
        anti_spam = self.cleaned_data.get('anti_spam')
        if anti_spam:
            self.add_error('anti_spam', 'spam comment')
