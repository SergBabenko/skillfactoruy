from django_filters import FilterSet, ModelChoiceFilter, CharFilter, DateFilter, DateRangeFilter
from .models import Author
from django import forms


class PostFilter(FilterSet):
    author = ModelChoiceFilter(queryset=Author.objects.all(), label="Автор", empty_label="Все")
    title = CharFilter(label="Заголовок", lookup_expr="iregex")
    text = CharFilter(label="Содержание", lookup_expr="iregex")

    date_range = DateRangeFilter(
        field_name='created_at',
        label='Период',
        empty_label='Выберите период',
    )
    # Позже указанной даты (больше или равно)
    added_after = DateFilter(
        field_name='created_at',
        lookup_expr='gte',
        label='Дата (от)',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    # Раньше указанной даты (меньше или равно)
    added_before = DateFilter(
        field_name='created_at',
        lookup_expr='lte',
        label='Дата (до)',
        widget=forms.DateInput(attrs={'type': 'date'})
    )


    # class Meta:
    #     model = Post
    #     fields = {
    #         'author': ['exact'],
    #         'title': ['iregex'],
    #         'text': ['iregex'],
    #
    #     }