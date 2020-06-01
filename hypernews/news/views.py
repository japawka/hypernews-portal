# from django.shortcuts import render
# from django.http import HttpResponse, Http404
# from django.views import View
# import json
# import itertools
# import datetime
#
# with open("news.json", "r") as json_file:
#     news_from_json = json.load(json_file)
#
#
# class MainPageView(View):
#     def get(self, request, *args, **kwargs):
#         text = "Coming soon"
#         return HttpResponse(text)
#
#
# class NewsMainView(View):
#     def get(self, request, *args, **kwargs):
#         news = news_from_json
#         formatted_news = {}
#         for key, group in itertools.groupby(news,
#                                             lambda x: datetime.datetime.strptime(x['created'],
#                                                                                  '%Y-%m-%d %H:%M:%S').date()):
#             for item in group:
#                 if str(key) in formatted_news:
#                     formatted_news[str(key)].append(item)
#                 else:
#                     formatted_news[str(key)] = [item]
#         return render(request, 'news_main.html', {'news': dict(sorted(formatted_news.items(), reverse=True))})
#
#
# class NewsDetailView(View):
#     def get(self, request, *args, **kwargs):
#         art_link = int(kwargs['link'])
#         art = [n for n in news_from_json if n["link"] == art_link][0]
#         context = {
#             'title': art["title"],
#             'text': art["text"],
#             'created': art['created']
#         }
#         return render(request, 'news_detail.html', context)

from django.shortcuts import render, redirect

from django.views.generic.base import View
from django.http.response import HttpResponse
import os
import json
import itertools
import datetime
import random


class ComingSoonView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'main.html')


class NewsView(View):
    def get(self, request, *args, **kwargs):
        news = get_json_info()
        for item in news:
            if int(item['link']) == int(kwargs['link']):
                return render(request, 'news.html', item)



class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        news = get_json_info()
        found = request.GET.get('q')
        print(found)
        formatted_news = {}
        for key, group in itertools.groupby(news,
                                            lambda x: datetime.datetime.strptime(x['created'],
                                                                                 '%Y-%m-%d %H:%M:%S').date()):
            for item in group:
                if str(key) in formatted_news:
                    formatted_news[str(key)].append(item)
                else:
                    formatted_news[str(key)] = [item]

        return render(request, 'welcome.html', {'found': found, 'news': dict(sorted(formatted_news.items(), reverse=True))})


class CreateNewsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'create.html')

    def post(self, request, *args, **kwargs):
        news = get_json_info()

        title = request.POST.get('title')
        text = request.POST.get('text')
        link = random.randint(1000000, 999999999)
        created = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_news = {"title": title, 'text': text, 'link': link, 'created': created}
        news.append(new_news)
        put_json_info(news)
        return redirect('/news')



def get_json_info():
    # module_dir = os.path.dirname(__file__)
    # file_path = os.path.join(module_dir, 'news.json')
    with open("news.json", "r") as json_file:
        news = json.load(json_file)
    return news

def put_json_info(news):

    with open("news.json", "w") as json_file:
        json.dump(news, json_file)
    print(f'item: {news} created!')