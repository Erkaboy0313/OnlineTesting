from django import template
from app.models import Answers , Test, Attempt
register = template.Library()

@register.simple_tag
def score(object):
    test = Test.objects.filter(block=object)
    true = ''
    for ob in test:
        true += str(Answers.objects.filter(attempt = ob, correct=True).count())+'/'
    return true[:-1]

@register.simple_tag
def subjects(object):
    test = Test.objects.filter(block=object)
    subject = ''
    for i in test:
        subject += i.subject_category.name+'/'
    return subject[:-1]

@register.simple_tag
def tottal(object):
    test = Test.objects.filter(block=object)
    true = ''
    for ob in test:
        true += str(Answers.objects.filter(attempt = ob).count())+'/'
    return true[:-1]

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

