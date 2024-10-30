from django.shortcuts import render
from django.http import HttpResponse
import json
from .models import Article
import plotly.express as px
from django.db import models
from collections import defaultdict


# Create your views here
def home(request):
    articles = Article.objects.all()
    distinct_countries = Article.objects.values_list('country', flat=True).distinct()
    distinct_pestles = list(Article.objects.values_list('pestle', flat=True).distinct().exclude(pestle='').order_by('pestle'))
    sectors = [article.sector for article in articles if article.sector]
    sectors = set(sectors)
    sectors = list(sectors)

    distinct_countries_list = list(distinct_countries)
    context = {
        "distinct_countries_list":distinct_countries_list,
        "distinct_pestles": distinct_pestles,
        "sectors":sectors
    }

    return render(request,"dashboard.html",context)




#views about sectar pie chart
def sector_pie_filter(request):
    if request.method == "POST":    
        country_name = request.POST.get("country")
        if country_name == "@":
            articles = Article.objects.all()
        else:
            articles = Article.objects.filter(country=country_name)
        
        if len(articles) == 0:
            return HttpResponse("No Insights present for this Country")
        sectors = [article.sector for article in articles if article.sector]
        sector_counts = defaultdict(int)
        for sector in sectors:
            sector_counts[sector] += 1

        sector_counts_dict = dict(sector_counts)

        labels = list(sector_counts_dict.keys())
        values = list(sector_counts_dict.values())

        total_articles = sum(values)
        print(total_articles)
        context = { "labels": labels, "values":values,"total_articles": total_articles}
        

    return render(request,"sector_pie.html",context)


    
def sector_pie(request):

    if request.method == "POST":
        articles = Article.objects.all()
        sectors = [article.sector for article in articles if article.sector]
        sector_counts = defaultdict(int)
        for sector in sectors:
            sector_counts[sector] += 1

        sector_counts_dict = dict(sector_counts)

        labels = list(sector_counts_dict.keys())
        values = list(sector_counts_dict.values())

        
        total_articles = sum(values)
        context = { "labels": labels, "values":values,"total_articles": total_articles}

    return render(request,"sector_pie.html",context)

    



#pestle bar chart

def pestle_bar(request):
    if request.method == "POST":
        articles = Article.objects.all()
        pestles = [article.pestle for article in articles if article.pestle]
        pestle_counts = defaultdict(int)
        for pestle in pestles:
            pestle_counts[pestle] += 1

        pestle_count_dict = dict(pestle_counts)

        labels = list(pestle_count_dict.keys())
        values = list(pestle_count_dict.values())

        
        total_articles = sum(values)
        context = { "labels": labels, "values":values,"total_articles": total_articles}

    return render(request,"pestle_bar.html",context)



#line chart that shows intensity of topic 
def intensity_line(request):
    if request.method == "POST":
        
        distinct_end_years = Article.objects.values_list('end_year', flat=True).distinct().exclude(end_year='').order_by('end_year')

            
        distinct_pestle = list(Article.objects.values_list('pestle', flat=True).distinct().exclude(pestle='').order_by('pestle'))

        intensity_data = [[0 for _ in range(len(distinct_end_years))] for _ in range(len(distinct_pestle))]

        for i, pestle in enumerate(distinct_pestle):
            for j, year in enumerate(distinct_end_years):
                intensity = Article.objects.filter(pestle=pestle, end_year=year).aggregate(average_intensity=models.Avg('intensity'))['average_intensity']
                if intensity is None:
                    intensity = 0
                intensity_data[i][j] = intensity

    context = {
                'labels': list(distinct_end_years),  
                'topics': distinct_pestle,  
                'intensity_data': intensity_data,
            }
    return render(request, 'intensity_line.html', context)

def data_table(request):
    if request.method == "POST":
        country_value = request.POST.get("country_name")
        sector_value  = request.POST.get("sector_name")
        data = list(Article.objects.all())[:20]

        
        
    context = { "data" : data }
    return render(request,"table.html",context)

def data_table_filter(request):
    if request.method == "POST":
        country_value = request.POST.get("country_name")
        sector_value  = request.POST.get("sector_name")
        data = Article.objects.all()
        
        if country_value and country_value != '@':
            data = data.filter(country=country_value)

        if sector_value and sector_value != '@':
            data = data.filter(sector=sector_value)


        if data:

            context = { "data" : data }

        else:
            return HttpResponse('<h2 class="text-center text-gray-400 text-xl mt-4">No rows with the following filters</h2>')
    return render(request,"table.html",context)


#method to store json data in django modal
"""def save_data(request):
    payloads = json.loads(request.body)
    Article.objects.all().delete()
    for payload in payloads:
        insight = Article(
                end_year=payload['end_year'],
                intensity=payload['intensity'],
                sector=payload['sector'],
                topic=payload['topic'],
                insight=payload['insight'],
                url=payload['url'],
                region=payload['region'],
                start_year=payload['start_year'],
                impact=payload['impact'],
                added=payload['added'], 
                published=payload['published'],
                country=payload['country'],
                relevance=payload['relevance'],
                pestle=payload['pestle'],
                source=payload['source'],
                title=payload['title'],
                likelihood=payload['likelihood']
            )
        insight.save()

    
    return HttpResponse("data rendered")
"""