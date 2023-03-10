import django_filters
from .models import Opinions


""" class OpinionsFilter(django_filters.FilterSet):
    opinion = 
    author = django_filters.ModelChoiceFilter(queryset=Opinions.objects.all())
    recommended = django_filters.ModelChoiceFilter(queryset=Opinions.objects.all())
    stars = django_filters.ModelChoiceFilter(queryset=Opinions.objects.all())
    trust = django_filters.ModelChoiceFilter(queryset=Opinions.objects.all())
    opinion_date = django_filters.ModelChoiceFilter(queryset=Opinions.objects.all())
    buy_date = django_filters.ModelChoiceFilter(queryset=Opinions.objects.all())
    useful_counter = django_filters.ModelChoiceFilter(queryset=Opinions.objects.all())
    unuseful_counter = django_filters.ModelChoiceFilter(queryset=Opinions.objects.all())
    opinion_desc = django_filters.ModelChoiceFilter(queryset=Opinions.objects.all())
    pros = django_filters.ModelChoiceFilter(queryset=Opinions.objects.all())
    cons = django_filters.ModelChoiceFilter(queryset=Opinions.objects.all())
    amount_pros = django_filters.ModelChoiceFilter(queryset=Opinions.objects.all())
    amount_cons = django_filters.ModelChoiceFilter(queryset=Opinions.objects.all())

    class Meta:
        model = Opinions
        fields =['recommended']
    """


class OpinionsFilter(django_filters.FilterSet):
    RECOMMENDED_CHOICES = [
        ('', 'Brak'),
        ('Polecam', 'Polecam'),
        ('Nie polecam', 'Nie polecam'),
    ]
    TRUST_CHOICES = [
        (' ', 'Niepotwierdzona'),
        ('Opinia potwierdzona zakupem', 'Potwierdzona'),
    ]
    opinion_id = django_filters.CharFilter(field_name='opinion_id',lookup_expr='icontains',  label='Opinion ID')
    author = django_filters.CharFilter(field_name='author', lookup_expr='icontains', label='Author')
    recommended = django_filters.MultipleChoiceFilter(choices=RECOMMENDED_CHOICES,field_name='recommended',label='Recommended')
    stars = django_filters.RangeFilter(field_name='stars', lookup_expr='icontains', label='Stars')
    trust = django_filters.ChoiceFilter(field_name='trust', choices=TRUST_CHOICES, label='Trust')
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

   