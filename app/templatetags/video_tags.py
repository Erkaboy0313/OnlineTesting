from django import template
from app.models import Answers
register = template.Library()

@register.simple_tag
def score(object):
    answers = Answers.objects.filter(attempt = object, correct = True).count()
    return answers

@register.simple_tag
def tottal(object):
    true = Answers.objects.filter(attempt = object).count()
    return true
