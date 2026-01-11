from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['author'].empty_label = 'Выберите Автора'

    class Meta:
        model = Post
        fields = ['author', 'post_type', 'title', 'text', 'category']
        labels = {
            'author': 'Автор',
            'title':'Заголовок',
            'text':'Содержание',
            'category': 'Категории',
            'post_type': 'Тип публикации'
        }

        widgets = {
            'text': forms.Textarea(attrs={'class':'form-textarea', 'rows':'4', 'cols':'38'}),
        }