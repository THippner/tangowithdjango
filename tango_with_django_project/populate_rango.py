__author__ = 'khorm'

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()

import random

from rango.models import Category, Page


def populate():
    python_cat = add_cat('Python')

    add_page(cat=python_cat,
             title="Official Python Tutorial",
             url="http://docs.python.org/2/tutorial/")

    add_page(cat=python_cat,
             title="How to think like a Computer Scientist",
             url="http://www.greenteapress.com/thinkpython/")

    add_page(cat=python_cat,
             title="Learn python in 10 minutes",
             url="http://www.korokithakis.net/tutorials/python/")

    django_cat = add_cat('Django')

    add_page(cat=django_cat,
             title="Official Django tutorial",
             url="https://docs.djangoproject.com/en/1.5/intro/tutorial01")

    add_page(cat=django_cat,
             title="Django Rocks",
             url="http://www.djangorocks.com/")

    add_page(cat=django_cat,
             title="How to Tango with Django",
             url="http://www.tangowithdjango.com/")

    frame_cat = add_cat('Other Frameworks')

    add_page(cat=frame_cat,
             title="Bottle",
             url="http://bootlepy.org/docs/dev/")

    add_page(cat=frame_cat,
             title="Flask",
             url="http://flask.pocoo.org")

    my_cat = add_cat('Tomasz Hippner')

    add_page(cat=my_cat,
             title="My Github tangowithdjango repository",
             url="https://github.com/THippner/tangowithdjango/commits/")

    add_page(cat=my_cat,
             title="My Pythonanywhere.com page",
             url="https://www.pythonanywhere.com/user/THippner/")

    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print "- {0} - {1}".format(str(c), str(p))


def add_page(cat, title, url):

    generate_views = random.randint(0, 100)
    p = Page.objects.get_or_create(category=cat, title=title, url=url, views=generate_views)[0]
    return p


def add_cat(name, views=0, likes=0):
    c = Category.objects.get_or_create(name=name, views=views, likes=likes)[0]

    if name == 'Python':
        c.views = 128
        c.likes = 64

    elif name == 'Django':
        c.views = 64
        c.likes = 32

    elif name == 'Other Frameworks':
        c.views = 32
        c.likes = 16

    else:
        pass

    c.save()
    return c


if __name__ == '__main__':
    print "Starting rango population script..."
    populate()


























