from tango_with_django_project.settings import MEDIA_URL
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Book, Category, Page, Video

# For an explanation of what is going on here, please refer to the TwD book.

def populate():
    python_pages = [
        {'title': 'Official Python Tutorial',
         'url':'http://docs.python.org/3/tutorial/',
         'views': 114,},
        {'title':'How to Think like a Computer Scientist',
         'url':'http://www.greenteapress.com/thinkpython/',
         'views': 53},
        {'title':'Learn Python in 10 Minutes',
         'url':'http://www.korokithakis.net/tutorials/python/',
         'views': 20} ]
    
    django_pages = [
        {'title':'Official Django Tutorial',
         'url':'https://docs.djangoproject.com/en/2.1/intro/tutorial01/',
         'views': 32},
        {'title':'Django Rocks',
         'url':'http://www.djangorocks.com/',
         'views': 12},
        {'title':'How to Tango with Django',
         'url':'http://www.tangowithdjango.com/',
         'views': 1258} ]
    
    java_pages = [
        {'title':'Java Tutorial',
         'url':'https://www.tutorialspoint.com/java/index.htm',
         'views': 45},
        {'title':'Java for Beginners',
         'url':'https://www.guru99.com/java-tutorial.html',
         'views': 189},
        {'title':'Java for kids',
         'url':'https://www.idtech.com/blog/java-for-kids-a-guide-for-parents-of-new-coders',
         'views': 12}

    ]
    
    python_videos = [
        {'title':'Python for Beginners - Learn Python in 1 Hour',
         'url':'https://www.youtube.com/embed/watch?v=kqtD5dpn9C8',
         'views': 13},
        {'title':'Intermediate Python Programming Course',
         'url':'https://www.youtube.com/embed/watch?v=HGOBQPFzWKo',
         'views': 9} ]
    
    django_videos = [
        {'title':'Django Tutorial for beginners',
         'url':'https://www.youtube.com/embed/watch?v=rHux0gMZ3Eg',
         'views': 13},
        {'title':'Creating a website with Django',
         'url':'https://www.youtube.com/embed/watch?v=ZsJRXS_vrw0',
         'views': 9} ]
    
    java_videos = [
        {'title':'Java Tutorial for beginners',
         'url':'https://www.youtube.com/embed/watch?v=eIrMbAQSU34',
         'views': 83},
        {'title':'Classes and Objects',
         'url':'https://www.youtube.com/embed/watch?v=Mm06BuD3PlY',
         'views': 19} ]

    python_books= [
        {'title':'Python Crash Course',
         'url':'https://www.amazon.co.uk/Python-Crash-Course-2nd-Edition/dp/1593279280/ref=sr_1_4?dchild=1&keywords=python&qid=1628085495&sr=8-4',
         'picUrl': MEDIA_URL + 'Python_crashcourse.jpg',
         'views': 19},
        #{'title':'Classes and Objects',
        # 'url':'https://www.youtube.com/embed/watch?v=Mm06BuD3PlY',
        # 'picUrl':'https://www.youtube.com/embed/watch?v=eIrMbAQSU34',
        # 'views': 19} ]
    ]


    
    cats = {'Python': {'pages': python_pages, 'views': 128, 'likes': 64, 'videos': python_videos, 'vidviews': 128, 'vidlikes': 64, 'books': python_books, 'boviews': 128, 'bolikes': 64},
            'Django': {'pages': django_pages, 'views': 64, 'likes': 32, 'videos': django_videos, 'vidviews': 128, 'vidlikes': 64, 'books': python_books, 'boviews': 128, 'bolikes': 64},
            'Java': {'pages': java_pages, 'views': 66, 'likes': 35, 'videos': java_videos, 'vidviews': 189, 'vidlikes': 164, 'books': python_books, 'boviews': 128, 'bolikes': 64},
            
    }
    
    for cat, cat_data in cats.items():
        c = add_cat(cat, views=cat_data['views'], likes=cat_data['likes'])
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'], views=p['views'])
        for x in cat_data['videos']:
            add_video(c, x['title'], x['url'], views=x['views'])
        for y in cat_data['books']:
            add_book(c, y['title'], y['url'], y['picUrl'], views=y['views'])
    
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')

def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    p.save()
    return p

def add_video(cat, title, url, views=0):
    p = Video.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    p.save()
    return p

def add_book(cat, title, url, picUrl, views=0):
    p = Book.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.picUrl = picUrl
    p.views=views
    p.save()
    return p

def add_cat(name, views=0, likes=0):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c

# Start execution here!
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()