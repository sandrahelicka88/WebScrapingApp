from django.shortcuts import render
from bs4 import BeautifulSoup
from requests.compat import quote_plus
from . import models
import requests

# Create your views here.

BASE_CRAIGSLIST_URL = 'https://london.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'
def home(request):
    return render(request, 'base.html',{})

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    post_listings = soup.find_all('li', {'class': 'result-row'})
    

    final_posting = []
    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'No price'
        if post.find(class_='result-image').get('data-ids'):
            post_img_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_img_url = BASE_IMAGE_URL.format(post_img_id)
        else:
            post_img_url = 'https://london.craigslist.org/hss/d/london-office-cleaning-wanted-genuine/7067743388.html'
    

        final_posting.append((post_title, post_url, post_price, post_img_url))
    
    front_end = {
        'search': search,
        'final_posting': final_posting,
    }

    return render(request, 'my_app/new_search.html',front_end)
