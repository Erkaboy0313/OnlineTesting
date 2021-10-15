from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class Profile(models.Model):
    USER_TYPE = (
        ('Talaba','Talaba'),
        ('Abiturient','Abiturient'),
        ("O'qituvchi","O'qituvchi")
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    status = models.BooleanField(default=True)
    image = models.ImageField(upload_to = 'user_images', blank=True, null = True)
    user_type = models.CharField(max_length=10 , choices=USER_TYPE , default='Unset')
    city = models.CharField(max_length=20,null=True , blank=True)

    @property
    def imageURL(self):
        try:
            return self.image.url
        except:
            return ''
    
    def __str__(self):
        return self.user.username


class Subject(models.Model):
    name = models.CharField(max_length=200, null=True)
    image = models.ImageField(upload_to='subject_images', null=True, blank=True)
    description = models.TextField(null=True)

    @property
    def imageURL(self):
        try:
            return self.image.url
        except:
            return ''

    def __str__(self):
        return self.name + " " + str(self.id)


class Subject_categories(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    image = models.ImageField()
    description = models.TextField(null=True)

    @property
    def imageURL(self):
        try:
            return self.image.url
        except:
            return ''

    def __str__(self):
        return self.name + " " + str(self.id)


class Question(models.Model):
    subject = models.ForeignKey(Subject_categories, on_delete=models.SET_NULL, null=True)
    question = RichTextUploadingField(blank=True, null=True)
    var1 = RichTextUploadingField(blank=True, null=True)
    var2 = RichTextUploadingField(blank=True, null=True)
    var3 = RichTextUploadingField(blank=True, null=True)
    var4 = RichTextUploadingField(blank=True, null=True)
    ans = RichTextUploadingField(blank=True, null=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id}-test {self.subject.name}"


class Test(models.Model):
    status = models.BooleanField(default=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    subject_category = models.ForeignKey(Subject_categories, on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True)
    started_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject_category.name


class Test_files(models.Model):
    subject = models.ForeignKey(Subject_categories, on_delete=models.CASCADE, null=True)
    test_file = models.FileField(upload_to='test_files')

    @property
    def fileURL(self):
        try:
            return self.test_file.url
        except:
            return ''


class Answers(models.Model):
    attempt = models.ForeignKey(Test, on_delete=models.CASCADE, null=True, related_name='test_subject')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    user_asnwer = models.CharField(max_length=200, null=True)
    correct = models.BooleanField(default=False)

    def __srt__(self):
        return self.test.subject_category.name


class Comment(models.Model):
    subject = models.ForeignKey(Subject_categories, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    comment = RichTextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ' ' + self.comment[0:10]

    @property
    def time(self):
        return self.created_at.strftime('%d-%M-%Y')
