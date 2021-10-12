from django.contrib import admin
from .models import Subject, Question, Answers, Test, Subject_categories, Comment , Test_files


admin.site.register(Subject)
admin.site.register(Subject_categories)
admin.site.register(Question)
admin.site.register(Answers)
admin.site.register(Test)
admin.site.register(Comment)
admin.site.register(Test_files)