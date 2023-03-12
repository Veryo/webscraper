import django_filters
from django_filters import FilterSet, MultipleChoiceFilter
from django_filters.widgets import CSVWidget
from django import forms
from .models import Opinions

class OpinionsFilter(django_filters.FilterSet):
    opinion_id = django_filters.CharFilter(field_name='opinion_id',lookup_expr='icontains',  label='Opinion ID')
    author = django_filters.CharFilter(field_name='author', lookup_expr='icontains', label='Author')
    recommended = django_filters.AllValuesMultipleFilter(field_name='recommended', label='Recommended', widget=forms.CheckboxSelectMultiple(attrs={'class': 'list-unstyled'}))
    stars = django_filters.RangeFilter(field_name='stars',lookup_expr='icontains', label='Stars',)
    trust = django_filters.AllValuesMultipleFilter(field_name='trust', label='Trust', widget=forms.CheckboxSelectMultiple(attrs={'class': 'list-unstyled'}))
    opinion_date = django_filters.CharFilter(field_name='opinion_date', lookup_expr='icontains', label='Opinion Date')
    buy_date = django_filters.CharFilter(field_name='buy_date', lookup_expr='icontains', label='Buy Date')
    useful_counter = django_filters.RangeFilter(field_name='useful_counter', lookup_expr='icontains', label='Useful Counter')
    unuseful_counter = django_filters.CharFilter(field_name='unuseful_counter', lookup_expr='icontains', label='Unuseful Counter')
    opinion_desc = django_filters.CharFilter(field_name='opinion_desc', lookup_expr='icontains', label='Opinion Description')
    pros = django_filters.CharFilter(field_name='pros', lookup_expr='icontains', label='Pros')
    cons = django_filters.CharFilter(field_name='cons', lookup_expr='icontains', label='Cons')
    amount_pros = django_filters.RangeFilter(field_name='amount_pros', label='Amount of Pros')
    amount_cons = django_filters.RangeFilter(field_name='amount_cons', label='Amount of Cons')
    order_by = django_filters.OrderingFilter(
        fields=(
            ('opinion_id', 'opinion_id'),
            ('author', 'author'),
            ('recommended', 'recommended'),
            ('stars', 'stars'),
            ('trust', 'trust'),
            ('opinion_date', 'opinion_date'),
            ('buy_date', 'buy_date'),
            ('useful_counter', 'useful_counter'),
            ('unuseful_counter', 'unuseful_counter'),
            ('opinion_desc', 'opinion_desc'),
            ('pros', 'pros'),
            ('cons', 'cons'),
            ('amount_pros', 'amount_pros'),
            ('amount_cons', 'amount_cons'),
        ),
        label='Sort by'
    )
 
   