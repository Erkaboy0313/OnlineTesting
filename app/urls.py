from os import name
from django.urls import path
from .views import createtest, adminDashboard, log_in, log_out, index, subject, \
    test, register, users, home, result, delete_user, start, score, subject_categories, comment, \
    view_categories, add_file, update_test, url_test , userpage , allusers , changestatus

urlpatterns = [
    path('', index, name='index'),
    path('register/' , register, name='register'),
    path('login/', log_in, name='log_in'),
    path('log_out/' , log_out , name='log_out'),

    path('add_file/',add_file,name='add_file'),
    path('dashboard/',adminDashboard,name='dashboard'),
    path('subject/',subject,name='subject'),
    path('subject_categories/<int:id>/',subject_categories,name='subject_categories'),
    path('users/',users, name='users'),
    path('delete_user/<int:id>/',delete_user, name='delete_user'),

    path('check/',test,name='check'),

    path('test/<int:id>/',home,name='test'),
    path('result/',result,name='result'),
    path('scores/<int:id>/',score,name='score'),
    path('start/',start,name='start'),
    path('comment/<int:id>/',comment,name='comment'),

    path('categories/<int:id>/', view_categories, name='subjects'),
    path('update_test/', update_test, name='update_test'),
    path('url_test/', url_test, name='url_test'),
    path('allusers/', allusers, name='allusers'),
    path('userpage/<int:id>/', userpage, name='userpage'),
    path('changestatus/', changestatus, name='changestatus'),
]