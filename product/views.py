from django.shortcuts import render,redirect
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests
from . models import Product,Opinions
from django.db.models import Count,Sum
import csv
import xlwt
import json

from .forms import UrlForm

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
    name = soup.find(class_='product-top__product-info__name js_product-h1-link js_product-force-scroll js_searchInGoogleTooltip default-cursor').text 
    product = Product.objects.create(name=name,avg_stars = avg_stars)
    
    try:
        while True:
            user_reviews = soup.find_all(class_='user-post user-post__card js_product-review')
            for review in user_reviews:
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
                product = product,
                author=author,
                recommended=recommended,
                stars=stars,
                trust=trust,
                opinion_date=opinion_date,
                buy_date=buy_date,
                useful_counter=useful_counter,
                unuseful_counter=unuseful_counter,
                opinion_desc=opinion_desc,
                pros=pros,
                cons=cons,
                amount_pros = amount_pros,
                amount_cons = amount_cons
                )
            
            new_url = soup.find(class_='pagination__item pagination__next').get('href')
            url= 'https://www.ceneo.pl'+ new_url
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
           
    except:
        pass

def add_product(request):
    if request.method == 'POST':
        form = UrlForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['your_name']
            create_model_instance(url)
    else:
        form = UrlForm()
    return render(request, 'product/add_product.html', {'form': form})

def product_list(request):
    products = Product.objects.annotate(num_opinions=Count('opinions'),
                                         total_pros=Sum('opinions__amount_pros'),
                                         total_cons=Sum('opinions__amount_cons'))
    return render(request, 'product/product_list.html', {'products': products})

def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    opinions = Opinions.objects.filter(product=pk)
    return render(request, 'product/product_detail.html', {'product': product, 'opinions': opinions})

