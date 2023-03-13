from django.shortcuts import render,redirect
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests
from . models import Product,Opinions
from django.db.models import Count,Sum
from .filters import OpinionsFilter
from django.urls import reverse
import csv
import codecs
import json
from django.core import serializers
from functools import wraps
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import smart_str
from .forms import UrlForm
from django.contrib import messages



def try_except_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            return ""
    return wrapper


@try_except_decorator
def find_recommended(review):
    recommended = review.find(class_="recommended")
    if recommended:
        return recommended.text
    not_recommended = review.find(class_="not-recommended")
    if not_recommended:
        return not_recommended.text
    return ""

@try_except_decorator
def trust_buy(review):
    return review.find(class_="review-pz").find('em').text

@try_except_decorator
def find_date(review, index):
    return review.find(class_="user-post__published").find_all('time')[index].get('datetime')

def extract_pros_cons(review):
    i = 0
    pros = ""
    cons = ""
    amount_pros = 0
    amount_cons = 0
    try:
        if review.find(class_='review-feature__title review-feature__title--positives').text =="Zalety":
            pros_items = review.find_all(class_="review-feature__col")[i].find_all(class_='review-feature__item')
            pros = " ".join([item.text for item in pros_items])
            i += 1
            amount_pros = len(pros_items)
    except:
        pass
    try:
        cons_items = review.find_all(class_="review-feature__col")[i].find_all(class_='review-feature__item')
        cons = " ".join([item.text for item in cons_items])
        amount_cons = len(cons_items)
    except:
        pass
    return (pros, cons,amount_pros,amount_cons)

def create_model_instance(request):
    response = requests.get(request)
    soup = BeautifulSoup(response.text, "html.parser")
   
    avg_stars = soup.find(class_='product-review__score').get('content')
    name = soup.find(class_="product-top__title").find('h1').text
    product = Product.objects.create(name=name,avg_stars = avg_stars)
    
    try:
        while True:
            user_reviews = soup.find_all(class_='user-post user-post__card js_product-review')
            for review in user_reviews:
                opinion_id = review.get('data-entry-id')
                author = review.find(class_="user-post__author-name").text
                recommended = find_recommended(review)
                stars = review.find(class_="user-post__score-count").text
                trust = trust_buy(review)
                opinion_date = find_date(review,0)
                buy_date = find_date(review,1)
                useful_counter = review.find(class_="js_product-review-usefulness vote").find('button').get('data-total-vote')
                unuseful_counter = review.find(class_="js_product-review-usefulness vote").find_all('button')[1].get('data-total-vote')
                opinion_desc = review.find(class_="user-post__text").text
                pros,cons,amount_pros,amount_cons = extract_pros_cons(review)
                Opinions.objects.create(
                opinion_id = opinion_id,
                product = product,
                author = author,
                recommended = recommended,
                stars = stars,
                trust = trust,
                opinion_date = opinion_date,
                buy_date = buy_date,
                useful_counter = useful_counter,
                unuseful_counter = unuseful_counter,
                opinion_desc = opinion_desc,
                pros = pros,
                cons = cons,
                amount_pros = amount_pros,
                amount_cons = amount_cons
                )
            
            new_url = soup.find(class_='pagination__item pagination__next').get('href')
            url= 'https://www.ceneo.pl'+ new_url
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
    except:
        return product.pk

def add_product(request):
    if request.method == 'POST':
        form = UrlForm(request.POST)
        if form.is_valid():
            url = "https://www.ceneo.pl/"
            url += form.cleaned_data['id']
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser") 
            if response.ok  and soup.find(class_='product-review__link link link--accent js_clickHash js_seoUrl') ==None:
                pk = create_model_instance(url)
                return redirect('product_details', pk=pk)
            else:
                messages.error(request,'The product does not exist or it has no opinions')
                return redirect('add_product')
    else:
        form = UrlForm()
    return render(request, 'product/add_product.html', {'form': form})

def product_list(request):
    products = Product.objects.annotate(num_opinions=Count('opinions'),
                                         total_pros=Sum('opinions__amount_pros'),
                                         total_cons=Sum('opinions__amount_cons'))
    return render(request, 'product/product_list.html', {'products': products})


def download_json(request,pk):
    product = Product.objects.get(pk=pk)
    opinions_queryset = Opinions.objects.filter(product=pk)
    opinions_json = json.dumps(json.loads(serializers.serialize('json', opinions_queryset)), indent=4, ensure_ascii=False)
    
    response = HttpResponse(opinions_json, content_type='application/json')
    response['Content-Disposition'] = f'attachment; filename="{product.name} opinions.json"'
    
    return response

def download_xml(request,pk):
    product = Product.objects.get(pk=pk)
    opinions_queryset = Opinions.objects.filter(product=pk)
    opinions_xml = serializers.serialize('xml', opinions_queryset)
    
    response = HttpResponse(opinions_xml, content_type='application/xml')
    response['Content-Disposition'] = f'attachment; filename="{product.name} opinions.xml"'
    
    return response

def download_csv(request, pk):
    product = Product.objects.get(pk=pk)
    opinions_queryset = Opinions.objects.filter(product=pk)
    
    # Set up the response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{product.name} opinions.csv"'

    response.write(codecs.BOM_UTF8)
    # Set up the CSV writer
    writer = csv.writer(response)
    
    # Write the header row
    header_row = ['Opinion ID', 'Product', 'Author', 'Recommended', 'Stars', 'Trust', 'Opinion Date', 'Buy Date', 'Useful Counter', 'Unuseful Counter', 'Opinion Desc', 'Pros', 'Cons', 'Amount Pros', 'Amount Cons']
    writer.writerow(header_row)
    
    # Write the data rows
    for opinion in opinions_queryset:
        row = [
            opinion.opinion_id, opinion.product, opinion.author, opinion.recommended, opinion.stars, opinion.trust,
            opinion.opinion_date, opinion.buy_date, opinion.useful_counter, opinion.unuseful_counter, opinion.opinion_desc,
            opinion.pros, opinion.cons, opinion.amount_pros, opinion.amount_cons
        ]
        writer.writerow(row)

    return response

def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    opinions_queryset = Opinions.objects.filter(product=pk)
    opinions_filter = OpinionsFilter(request.GET, queryset=opinions_queryset)
    opinions = opinions_filter.qs
    form = opinions_filter.form
    return render(request, 'product/product_detail.html', {'product': product, 'opinions': opinions,'form':form,})

def catch_does_not_exist(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ObjectDoesNotExist:
            return 0
    return wrapper

@catch_does_not_exist
def count_recommendations(product_id, recommendation):
    return Opinions.objects.filter(product=product_id, recommended=recommendation).count()

@catch_does_not_exist
def count_stars(product_id, stars):
    return Opinions.objects.filter(product=product_id, stars=stars).count()

def charts(request, pk):
    product = Product.objects.get(pk=pk)
    polecam_count = count_recommendations(pk, 'Polecam')
    nie_polecam_count = count_recommendations(pk, 'Nie polecam')
    empty_count = count_recommendations(pk, '')
    one_star = count_stars(pk, '1/5')
    two_star = count_stars(pk, '2/5')
    three_star = count_stars(pk, '3/5')
    four_star = count_stars(pk, '4/5')
    five_star = count_stars(pk, '5/5')
    return render(request, 'product/product_charts.html', {'polecam_count': polecam_count,
                                                           'nie_polecam_count': nie_polecam_count,
                                                           'empty_count': empty_count,
                                                           'one_star': one_star,
                                                           'two_star': two_star,
                                                           'three_star': three_star,
                                                           'four_star': four_star,
                                                           'five_star': five_star,
                                                           'product':product})

def main(request):
    return render(request,'product/main.html')

def about(request):
    return render(request,'product/about.html')