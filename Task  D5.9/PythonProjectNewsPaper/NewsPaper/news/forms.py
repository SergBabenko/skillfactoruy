from django import forms
from .models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'text', 'category']
        labels = {
            'title':'Заголовок',
            'text':'Содержание',
            'category': 'Категории',
        }

        widgets = {
            'text': forms.Textarea(attrs={'class':'form-textarea', 'rows':'4', 'cols':'38'}),
        }