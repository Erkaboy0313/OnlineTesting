import json
from django.shortcuts import render, redirect
from .models import Subject, Question, Test, Answers, Subject_categories, Comment, Profile, Attempt
import os
from django.core.files.storage import default_storage
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
import docx2txt


def createtest(id, file):
    url = file.split('/')
    subject = Subject_categories.objects.get(id=id)
    path = default_storage.open(os.path.join(url[2], url[3]))
    text = docx2txt.process(path, str(path)[0:-8])
    for i in text.split('++++'):
        test = i.replace('\n', '').split('====')
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
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            print(username, password)
            user = authenticate(
                request=request,
                password=password,
                username=username
            )
            if user:
                login(request, user)
                return redirect(index)
    return render(request, 'app/login.html', {})


def log_out(request):
    logout(request)
    return redirect(log_in)


def register(request):
    if request.method == 'POST':
        form = Register(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST.get('username')
            password = request.POST.get('password1')
            user = authenticate(
                request=request,
                password=password,
                username=username
            )
            if user:
                Profile.objects.create(user=user)
                return redirect(log_in)
    return render(request, 'app/register.html', {})


def start_multiple_test(request, id1, id2, status=False):
    attempt = Attempt.objects.create(student=request.user)
    Test.objects.create(block=attempt, subject_category_id=id1)
    Test.objects.create(block=attempt, subject_category_id=id2)
    if status:
        Test.objects.create(block=attempt, subject_category_id=3)
        Test.objects.create(block=attempt, subject_category_id=4)
        Test.objects.create(block=attempt, subject_category_id=5)


@login_required(login_url='log_in')
def start(request):
    if request.method == 'POST':
        print(request.POST)
        id = request.POST.get('select')[0]
        id2 = request.POST.get('select1')[0]
        if len(request.POST) == 4:
            start_multiple_test(request, id, id2, status=True)
        else:
            start_multiple_test(request, id, id2)
        print(id, id2)
        return redirect(f'/test/{id}/')
    subject_category = Subject_categories.objects.all()
    context = {
        'subjects': subject_category
    }
    return render(request, 'app/start.html', context)


@login_required(login_url='log_in')
def start_single_test(request, id):
    subject = Subject_categories.objects.get(id=id)
    test = Test.objects.filter(subject_category=subject, block__student=request.user).order_by('-id')[0]
    if test:
        if test.block.status:
            answers = Answers.objects.filter(attempt=test).order_by('id')
            if len(answers) != 0:
                context = {
                    'checked_questions': answers,
                    'questions': '',
                    'test_id': test.id,
                    'next': '',
                    'prev': ''
                }
                is_next = Test.objects.filter(block_id=test.block.id).order_by('id')
                if len(is_next) > 1:
                    for i in len(is_next):
                        if is_next[i].subject_category.id == id:
                            if i == 0:
                                context['next'] = is_next[i + 1].subject_category.id
                            elif i == len(is_next) - 1:
                                context['prev'] = is_next[i - 1].subject_category.id
                            else:
                                context['next'] = is_next[i + 1].subject_category.id
                                context['prev'] = is_next[i - 1].subject_category.id

                        # if is_next[0].subject_category.id == id:
                        #     context['next'] = Test.objects.filter(block_id=test.block.id).order_by('id')[
                        #         1].subject_category.id
                        #     context['prev'] = ''
                        # else:
                        #     context['next'] = ''
                        #     context['prev'] = Test.objects.filter(block_id=test.block.id).order_by('id')[
                        #         0].subject_category.id
                print(context)
                return render(request, 'app/test.html', context)

            else:
                questions = Question.objects.filter(subject=subject, status=True).order_by('?')[:10]
                if len(questions) != 10:
                    test.delete()
                    return HttpResponse('Sorry we have no enought test to sart this test')
                for i in questions:
                    Answers.objects.create(attempt=test, question=i)
                print('Yangi test')
                context = {
                    'checked_questions': '',
                    'questions': questions,
                    'test_id': test.id,
                    'next': '',
                    'prev': ''
                }

                is_next = Test.objects.filter(block_id=test.block.id).order_by('id')
                if len(is_next) > 1:
                    for i in range(len(is_next)):
                        print(i)
                        if is_next[i].subject_category.id == id:
                            if i == 0:
                                print('Birintchi holat ------------------------')
                                context['next'] = is_next[i + 1].subject_category.id
                            elif i == len(is_next) - 1:
                                context['prev'] = is_next[i - 1].subject_category.id
                            else:
                                context['next'] = is_next[i + 1].subject_category.id
                                context['prev'] = is_next[i - 1].subject_category.id
                print('Yangi test chiqarildi')
                return render(request, 'app/test.html', context)
        else:
            attempt = Attempt.objects.create(student=request.user)
            test = Test.objects.create(block=attempt, subject_category_id=id)
            questions = Question.objects.filter(subject=subject, status=True).order_by('?')[:10]
            if len(questions) != 10:
                attempt.delete()
                return HttpResponse('Sorry we have no enought test to sart this test')
            for i in questions:
                Answers.objects.create(attempt=test, question=i)
            context = {
                'checked_questions': '',
                'questions': questions,
                'test_id': test.id,
            }
            print(context)
            return render(request, 'app/test.html', context)

    else:
        attempt = Attempt.objects.create(student=request.user)
        test = Test.objects.create(block=attempt, subject_category_id=id)
        questions = Question.objects.filter(subject=subject, status=True).order_by('?')[:10]
        if len(questions) != 10:
            attempt.delete()
            return HttpResponse('Sorry we have no enought test to sart this test')
        for i in questions:
            Answers.objects.create(attempt=test, question=i)
        context = {
            'checked_questions': '',
            'questions': questions,
            'test_id': test.id,
        }
        print(context)
        return render(request, 'app/test.html', context)


def adminDashboard(request):
    if request.user.is_staff:
        return render(request, 'app/dashboard.html')
    else:
        return redirect('index')


def subject(request):
    subjects = Subject.objects.all()
    if request.method == 'POST':
        add_file = Subject_Form(request.POST, request.FILES)
        if add_file.is_valid():
            name = request.POST.get('name')
            image = request.FILES.get('image')
            description = request.POST.get('description')
            Subject.objects.create(name=name, image=image, description=description)
            return redirect('dashboard')
        else:
            return HttpResponse("Error")
    context = {
        'subjects': subjects
    }

    return render(request, 'app/subjects.html', context)


def subject_categories(request, id):
    url = request.META.get('HTTP_REFERER')
    subject = Subject.objects.get(id=id)
    subject_categories = Subject_categories.objects.filter(subject=subject)
    if request.method == 'POST':
        add_file = Subject_categories_Form(request.POST, request.FILES)
        if add_file.is_valid():
            name = request.POST.get('name')
            image = request.FILES.get('image')
            description = request.POST.get('description')
            Subject_categories.objects.create(subject=subject, name=name, image=image, description=description)
            return HttpResponseRedirect(url)
        else:
            return HttpResponse("Error")
    context = {
        'subject_categories': subject_categories
    }
    return render(request, 'app/subject_categories.html', context)


def test(request):
    data = json.loads(request.body)
    test = Test.objects.get(id=data['test_id'])
    question = Question.objects.get(id=data['question_id'])
    answer = Answers.objects.get(attempt=test, question=question)
    answer.user_asnwer = data['value']
    if question.ans == data['value']:
        answer.correct = True
    answer.save()
    return JsonResponse({'status': 'ok'})


def users(request):
    users = User.objects.all()
    context = {
        'users': users
    }
    return render(request, 'app/tables.html', context)


def result(request):
    data = json.loads(request.body)
    print(data['test_id'])
    test = Test.objects.get(id=data['test_id']).block.id
    attempt = Attempt.objects.get(id=test)
    attempt.status = False
    attempt.save()
    return JsonResponse({'status': 'ok'})


def score(request, id):
    test = Test.objects.get(id=id).block.id
    at = Attempt.objects.get(id=test)
    tests = Test.objects.filter(block=at)
    comments = []
    form = Commentform()
    if len(tests) > 1:
        answers = Answers.objects.filter(attempt=tests[0]).order_by('id')
        answers1 = Answers.objects.filter(attempt=tests[1]).order_by('id')
        context = {
            'id': tests[0].subject_category.subject.id,
            'url_id': tests[0].subject_category.id,
            'ans': answers,
            'ans2': answers1,
            'comment': comments,
            'form': form,
            'subjects': tests,
        }
    else:
        answers = Answers.objects.filter(attempt=tests[0]).order_by('id')
        context = {
            'id': tests[0].subject_category.subject.id,
            'url_id': tests[0].subject_category.id,
            'ans': answers,
            'comment': comments,
            'form': form,
            'subjects': tests,
        }
    return render(request, 'app/result.html', context)


def delete_user(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return redirect('users')


def delete_test(request, id):
    url = request.META.get('HTTP_REFERER')
    Test.objects.get(id=id).delete()
    return HttpResponseRedirect(url)


def delete_attempt(request, id):
    url = request.META.get('HTTP_REFERER')
    Attempt.objects.get(id=id).delete()
    return HttpResponseRedirect(url)


@login_required(login_url='log_in')
def comment(request, id):
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


def view_categories(request, id):
    subjects = Subject_categories.objects.filter(subject_id=id)
    comments = Comment.objects.filter(subject_id=id).order_by('-id')
    form = Commentform()
    context = {
        'subject_name': subjects[0].subject.name,
        'subjects': subjects,
        'image': subjects[0].subject.imageURL,
        'comment': comments,
        'subject_id': subjects[0].subject.id,
        'form': form
    }
    return render(request, 'app/Add_category.html', context)


def add_file(request):
    url = request.META.get('HTTP_REFERER')
    sb = request.POST.get('test_file')
    subject = Subject_categories.objects.get(name=sb)
    file = Test_files()
    file.subject = subject
    file.test_file = request.FILES.get('file')
    file.save()
    file_url = file.fileURL
    createtest(subject.id, file_url)
    return HttpResponseRedirect(url)


def edit_test(request, id):
    questions = Question.objects.filter(subject_id=id)
    return render(request, 'app/edittest.html', {'tests': questions})


def url_test(request):
    url = request.META.get('HTTP_REFERER')
    for i in request.POST:
        print(request.POST[i])
        if request.POST[i].isdigit():
            id = int(request.POST[i])
            question = Question.objects.get(id=id)
            question.status = True
            question.save()
    return HttpResponseRedirect(url)


def userpage(request, id):
    profile = Profile.objects.get(user_id=id)
    attemp = Attempt.objects.filter(student=profile.user)
    # attemps = []
    # for a in attemp:
    #     res = []
    #     test = Test.objects.filter(block=a)
    #     for i in test:
    #         res.append(i)
    #     d = {
    #         'id':a.id,
    #         'attemp_t':res
    #     }
    #     attemps.append(d)
    if request.method == "POST":
        form = UpdateProfile(request.POST, request.FILES)
        if form.is_valid():
            profile.image = request.FILES.get('image')
            profile.city = request.POST.get('city')
            profile.user_type = request.POST.get('user_type')
            profile.save()
    else:
        form = UpdateProfile()
    return render(request, 'app/userpage.html', {'attemps': attemp, 'profile': profile, 'form': form})


def allusers(request):
    profiles = Profile.objects.all()
    return render(request, 'app/profile.html', context={'profiles': profiles})


def changestatus(request):
    data = json.loads(request.body)
    profile = Profile.objects.get(user_id=data['user_id'])
    print(profile.user.username)
    if profile.status:
        print('false')
        profile.status = False
        profile.save()
    else:
        print('True')
        profile.status = True
        profile.save()
    return JsonResponse({"status": 'ok'})


def chat(request, id):
    subjects = Subject_categories.objects.filter(id=id)
    subject = Subject_categories.objects.get(id=id)
    comments = Comment.objects.filter(subject=subject).order_by('-id')
    form = Commentform()
    context = {
        'id': id,
        'subjects': subjects,
        'comment': comments,
        'subject_id': subjects[0].subject.id,
        'form': form
    }
    return render(request, 'app/chat.html', context)
