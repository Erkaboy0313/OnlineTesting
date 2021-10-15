import json
from django.shortcuts import render,redirect
from .models import Subject, Question, Test, Answers, Subject_categories, Comment , Profile
import os
from django.core.files.storage import default_storage
from django.contrib.auth import authenticate, login,logout
from .forms import *
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
import docx2txt

def createtest(id,file):
    url = file.split('/')
    subject = Subject_categories.objects.get(id=id)
    path = default_storage.open(os.path.join(url[2],url[3]))
    text = docx2txt.process(path , str(path)[0:-8])
    for i in text.split('++++'):
        test = i.replace('\n','').split('====')
        question = Question.objects.create(subject=subject)
        question.question = test[0]
        question.var1 = str(test[1])[1:]
        question.var2 = test[2]
        question.var3 = test[3]
        question.var4 = test[4]
        question.ans = str(test[1])[1:]
        question.save()

def index(request):
    subjects = Subject.objects.all()
    context = {
        'subjects': subjects
    }
    return render(request, 'app/index.html', context)

def log_in(request):
    if request.method=='POST':
        form=Login(request.POST)
        if form.is_valid():
            username=request.POST.get('username')
            password=request.POST.get('password')
            print(username, password)
            user=authenticate(
                request=request,
                password=password,
                username=username
            )
            if user:
                login(request,user)
                return redirect(index)
    return render(request,'app/login.html', {} )
    
def log_out(request):
    logout(request)
    return redirect(log_in)
def register(request):
    if request.method == 'POST':
        form=Register(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST.get('username')
            password = request.POST.get('password1')
            user=authenticate(
                request=request,
                password=password,
                username=username
            )
            if user:
                Profile.objects.create(user = user)
                return redirect(log_in)
    return render(request,'app/register.html',{})
@login_required(login_url='login')
def start(request):
    if request.method == 'POST':
        id = request.POST.get('select')[0]
        return redirect(f'/test/{id}')
    subject_category = Subject_categories.objects.all()
    context = {
        'subjects': subject_category
    }
    return render(request, 'app/start.html', context)
@login_required(login_url='login')
def home(request,id):
    subject = Subject_categories.objects.get(id=id)
    try:
        test = Test.objects.filter(subject_category=subject , student = request.user).order_by('-id')[0]
    except:
        test = ''
    if test:
        if test.status:
            ansvers = Answers.objects.filter(attempt = test).order_by('id')
            print(ansvers)
            return render(request , 'app/test.html' , context={'checked_questions':ansvers,'questions':'','test_id':test.id})
        else:
            test = Test.objects.create(subject_category = subject , student = request.user)
    else:
        test = Test.objects.create(subject_category = subject , student = request.user)
    questions = Question.objects.filter(subject=subject, status=True).order_by('?')[:10]
    for i in questions:
        Answers.objects.create(attempt = test , question = i)
    return render(request,'app/test.html',context={'checked_questions':'','questions':questions,'test_id':test.id})
def adminDashboard(request):
    if request.user.is_staff:
        return render(request, 'app/dashboard.html')
    else:
        return redirect('index')
def subject(request):
    subjects = Subject.objects.all()
    if request.method == 'POST':
        add_file = Subject_Form(request.POST,request.FILES)
        if add_file.is_valid():
            name = request.POST.get('name')
            image = request.FILES.get('image')
            description = request.POST.get('description')
            Subject.objects.create(name=name,image=image,description=description)
            return redirect('dashboard')
        else:
            return HttpResponse("Error")
    context = {
        'subjects':subjects
    }

    return render(request , 'app/subjects.html' , context)
def subject_categories(request,id):
    url = request.META.get('HTTP_REFERER')
    subject = Subject.objects.get(id=id)
    subject_categories = Subject_categories.objects.filter(subject=subject)
    if request.method == 'POST':
        add_file = Subject_categories_Form(request.POST,request.FILES)
        if add_file.is_valid():
            name = request.POST.get('name')
            image = request.FILES.get('image')
            description = request.POST.get('description')
            add_test = Subject_categories.objects.create(subject=subject,name=name,image=image,description=description)
            return HttpResponseRedirect(url)
        else:
            return HttpResponse("Error")
    context = {
        'subject_categories':subject_categories
    }
    return render(request , 'app/subject_categories.html' , context)
def test(request):
    data = json.loads(request.body)
    test = Test.objects.get(id=data['test_id'])
    question = Question.objects.get(id = data['question_id'])
    answer = Answers.objects.get(attempt = test , question = question)
    answer.user_asnwer = data['value']
    if question.ans == data['value']:
        answer.correct = True
    answer.save()
    return JsonResponse({'status':'ok'})

def users(request):
    users=User.objects.all()
    context={
        'users':users
    }
    return render(request, 'app/tables.html', context)

def result(request):
    data = json.loads(request.body)
    print(data['test_id'])
    test = Test.objects.get(id = data['test_id'])
    test.status = False
    test.save()
    return JsonResponse({'status':'ok'})

def score(request,id):
    test = Test.objects.get(id = id)
    answers = Answers.objects.filter(attempt = test).order_by('id')
    comments = []
    form = Commentform()
    subjects = Subject_categories.objects.all()
    context={
        'id':test.subject_category.subject.id,
        'url_id':test.subject_category.id,
        'ans':answers,
        'comment': comments,
        'form': form,
        'subjects': subjects,
    }
    return render(request , 'app/result.html', context)

def delete_user(request,id):
    user = User.objects.get(id=id)
    user.delete()
    return redirect('users')

@login_required(login_url='login')
def comment(request,id):
    url = request.META.get('HTTP_REFERER')
    print(url)
    if request.method == 'POST':
        form = Commentform(request.POST)
        if form.is_valid():
            print(request.POST)
            subject = Subject_categories.objects.get(id=id)
            comment = Comment()
            comment.subject = subject
            comment.user = request.user
            comment.comment = request.POST.get('comment')
            comment.save()
            return HttpResponseRedirect(url)
    return HttpResponseRedirect(url)
def view_categories(request,id) :
    subjects = Subject_categories.objects.filter(subject_id = id)
    comments = Comment.objects.filter(subject_id = id).order_by('-id')
    form = Commentform()
    context = {
        'subject_name':subjects[0].subject.name,
        'subjects':subjects,
        'image':subjects[0].subject.imageURL,
        'comment':comments,
        'subject_id':subjects[0].subject.id,
        'form':form
    }
    return render(request , 'app/Add_category.html', context)
def add_file(request):
    url = request.META.get('HTTP_REFERER')
    sb = request.POST.get('test_file')
    subject = Subject_categories.objects.get(name=sb)
    file = Test_files()
    file.subject = subject
    file.test_file = request.FILES.get('file')
    file.save()
    file_url=file.fileURL
    createtest(subject.id,file_url)
    return HttpResponseRedirect(url)
def update_test(request):
    data = json.loads(request.body)
    questions = Question.objects.filter(subject_id = data['subject_id'])
    tests = []
    for q in questions:
        q = {
            'id':q.id,
            'q':q.question,
            'v1':q.var1,
            'v2':q.var2,
            'v3':q.var3,
            'v4':q.var4,
            'ans':q.ans,
            'status': q.status
        }
        tests.append(q)
    return JsonResponse({'tests':tests})
def url_test(request):
    print(request.POST)
    for i in request.POST:
        print(request.POST[i])
        if request.POST[i].isdigit():
            id = int(request.POST[i])
            question = Question.objects.get(id = id)
            question.status = True
            question.save()
    return HttpResponse({'status':'OK'})

def userpage(request,id):
    tests = Test.objects.filter(student = request.user)
    profile = Profile.objects.get(user_id = id)
    return render(request , 'app/userpage.html' , {'tests':tests , 'profile':profile})

def allusers(request):
    profiles = Profile.objects.all()
    return render(request,'app/profile.html',context={'profiles':profiles})


def chat(request, id):
    subjects = Subject_categories.objects.filter(id=id)
    subject = Subject_categories.objects.get(id = id)
    comments = Comment.objects.filter(subject= subject).order_by('-id')
    form = Commentform()
    context = {
        'id':id,
        'subjects': subjects,
        'comment': comments,
        'subject_id': subjects[0].subject.id,
        'form': form
    }
    return render(request, 'app/chat.html', context)