from django.shortcuts import render,redirect
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests
from django.db.models import Count,Sum
import csv
import codecs
import json
from django.core import serializers
from django.contrib import messages
import collections as co

from . models import Product,Opinions
from .forms import UrlForm
from .filters import OpinionsFilter
from .functions import *

def main(request):
    return render(request,'product/main.html')


def about(request):
    return render(request,'product/about.html')


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


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    opinions_queryset = Opinions.objects.filter(product=pk)

    opinions_filter = OpinionsFilter(request.GET, queryset=opinions_queryset)
    opinions = opinions_filter.qs
    form = opinions_filter.form

    if form.is_valid():
        pass
    else:
         messages.error(request,'Wrong Filtering Options')
    
    return render(request, 'product/product_detail.html', {'product': product, 'opinions': opinions,'form':form,})


def charts(request, pk):
    product = Product.objects.get(pk=pk)
    opinions_queryset = Opinions.objects.filter(product=pk)
    
    recomeded = co.Counter([x.recommended for x in opinions_queryset])
    recomend_labels = [k for k in recomeded]
    recomend_values = [v for k,v in recomeded.items()]

    stars = co.Counter([x.stars for x in opinions_queryset])
    star_lables = [k for k in stars]
    star_values = [v for k,v in stars.items()]

    context = {
        'product':product,
        'recomend_labels': recomend_labels,
        'recomend_values': recomend_values,
        'star_labels':star_lables,
        'star_values':star_values

    }

    return render(request, 'product/product_charts.html', context)


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
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{product.name} opinions.csv"'

    response.write(codecs.BOM_UTF8)
    writer = csv.writer(response)
    
    header_row = ['Opinion ID', 'Product', 'Author', 'Recommended', 'Stars', 'Trust', 'Opinion Date', 'Buy Date', 'Useful Counter', 'Unuseful Counter', 'Opinion Desc', 'Pros', 'Cons', 'Amount Pros', 'Amount Cons']
    writer.writerow(header_row)
    
    for opinion in opinions_queryset:
        row = [
            opinion.opinion_id, opinion.product, opinion.author, opinion.recommended, opinion.stars, opinion.trust,
            opinion.opinion_date, opinion.buy_date, opinion.useful_counter, opinion.unuseful_counter, opinion.opinion_desc,
            opinion.pros, opinion.cons, opinion.amount_pros, opinion.amount_cons
        ]
        writer.writerow(row)

    return response







