import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                                   'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page
def populate():
    # First, we will create lists of dictionaries containing the pages 11 # we want to add into each category. 12 # Then we will create a dictionary of dictionaries for our categories. 13 # This might seem a little bit confusing, but it allows us to iterate 14 # through each data structure, and add the data to our models.
    #her bir page'e views ekledim chp6 exercise.!
    python_pages = [
        {'title': 'Official Python Tutorial',
         'views':15,
        'url':'http://docs.python.org/3/tutorial/'},

        {'title':'How to Think like a Computer Scientist',
        'views':20,
        'url':'http://www.greenteapress.com/thinkpython/'},

        {'title':'Learn Python in 10 Minutes',
        'views':40,
        'url':'http://www.korokithakis.net/tutorials/python/'} ]
    django_pages = [
        {'title':'Official Django Tutorial',
         'views': 60,
        'url':'https://docs.djangoproject.com/en/2.1/intro/tutorial01/'},

        {'title':'Django Rocks',
         'views': 100,
        'url':'http://www.djangorocks.com/'},
        {'title':'How to Tango with Django',
         'views': 150,
        'url':'http://www.tangowithdjango.com/'} ]

    other_pages = [
        {'title':'Bottle',
         'views': 20,
         'url':'http://bottlepy.org/docs/dev/'},
        {'title':'Flask',
         'views': 5,
        'url':'http://flask.pocoo.org'} ]
    cats = {'Python': {'pages': python_pages,'views':128,'likes':64}, #chp 5 views and likes
            'Django': {'pages': django_pages,'views':64,'likes':32}, #chp5 ""  "" " """" "
            'Other Frameworks': {'pages': other_pages,'views':32,'likes':16} #chp5""""""""

            }

# If you want to add more categories or pages, 43 # add them to the dictionaries above. 44 45 # The code below goes through the cats dictionary, then adds each category, 46 # and then adds all the associated pages for that category.


    for cat, cat_data in cats.items():
        c = add_cat(cat,cat_data['views'],cat_data['likes']) #chp 5 views and likes acces to the values modified.
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'],p['views']) #vhp6 exercise ekledim viewsi


    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')
def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    p.save()
    return p

def add_cat(name,views=0,likes=0):#views likes added for chp5 ex
    c = Category.objects.get_or_create(name=name)[0]
    c.likes=likes #chp5
    c.views=views#chp5
    c.save()#chp5

    return c

    #start execution here.
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()
