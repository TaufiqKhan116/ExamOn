from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE

# Create your models here.
class UserAbstract(AbstractUser):
    username            = models.CharField(max_length=50, unique="True", blank=False)
    password            = models.CharField(max_length=200, blank=False)
    isStudent           = models.BooleanField(default=False)
    isQuestionSetter    = models.BooleanField(default=False)
    isAdmin             = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Student(models.Model):
    class Meta:
        unique_together = (('studentID',),)

    user        = models.OneToOneField(UserAbstract, null=True, blank=True, on_delete=models.CASCADE)
    name        = models.CharField(max_length=200, blank=True)
    email       = models.EmailField(blank=True)
    studentID   = models.IntegerField(blank=True)
    isVerified  = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.name


class QuestionSetter(models.Model):
    user        = models.OneToOneField(UserAbstract, null=True, blank=True, on_delete=models.CASCADE)
    name        = models.CharField(max_length=200, blank=True)
    email       = models.EmailField(blank=True)
    isVerified  = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.name


class Admin(models.Model):
    user    = models.OneToOneField(UserAbstract, null=True, blank=True, on_delete=models.CASCADE)
    name    = models.CharField(max_length=200, blank=True)
    email   = models.EmailField(blank=True)

    def __str__(self):
        return self.name

class Question(models.Model):
    class Meta:
        unique_together = (('group', 'question'),)

    setter      = models.ForeignKey(QuestionSetter, on_delete=models.CASCADE)
    group       = models.CharField(max_length=200, blank=False)
    question    = models.CharField(max_length=500, blank=False)
    marks        = models.FloatField(blank=True, null=True)
    isTrueFalse = models.BooleanField(default=False)
    isMCQ       = models.BooleanField(default=False)
    isFile      = models.BooleanField(default=False)

    # def __str__(self):
    #     return self.group

class GroupAttr(models.Model):
    class Meta:
        unique_together = (('group', ), )

    group       = models.CharField(max_length=200, blank=True)
    elapsedTime = models.FloatField(blank=True, null=True)
    passcode    = models.CharField(max_length=8, blank=True, null=True)
    isPublished   = models.BooleanField(default=False)

class TrueFalseQuestion(models.Model):
    question    = models.OneToOneField(Question, null=True, blank=True, on_delete=models.CASCADE)
    answer      = models.BooleanField(default=False)

class MCQQuestions(models.Model):
    question    = models.OneToOneField(Question, null=True, blank=True, on_delete=models.CASCADE)
    opt_1       = models.CharField(max_length=200)
    opt_2       = models.CharField(max_length=200)
    opt_3       = models.CharField(max_length=200)
    opt_4       = models.CharField(max_length=200)
    answer      = models.CharField(max_length=1)

class StudentQuestionMap(models.Model) :
    class Meta:
        unique_together = (('question', 'student'),)

    question    = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    student     = models.ForeignKey(Student, null=True, blank=True, on_delete=models.CASCADE)