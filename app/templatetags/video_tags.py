from django import template
from app.models import Answers , Test
register = template.Library()

@register.simple_tag
def score(object):
    answers = Answers.objects.filter(attempt = object, correct = True).count()
    return answers

@register.simple_tag
def tottal(object):
    true = Answers.objects.filter(attempt = object).count()
    return true

@register.simple_tag
def all(object):
    return Test.objects.filter(block__student = object.user).count()

@register.simple_tag
def rank(object):
    count = Answers.objects.filter(attempt__block__student = object.user).count()
    true = Answers.objects.filter(attempt__block__student = object.user , correct = True).count()
    if true and count:
        print(true/count*100)
        return round(((true/count)*100),1)
    else:
        return 0
