from django import template

register = template.Library()

def index(indexable, i):
    return indexable[i]

register.filter('index', index)