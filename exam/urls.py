from django.urls import path

from exam.views import *

app_name = 'exam'

urlpatterns = [
    path('', IndexView, name='index'),
    path('about/', AboutView, name='about'),
    path('contact/', ContactView, name='contact'),
    # path('examevent/', views.examevent, name='examevent'),

    # signup & signin views
    # path('signIn/', views.signInView, name='signIn'),
    # path('logout/', views.logoutView, name='logout'),
    # path('signUpStudent/', views.signUpStudent, name='signUpStudent'),
     path('instructorSignUp/', instructorSignUpView, name='instructorSignUp'),
     path('studentSignUp/', studentSignUpView, name='studentSignUp'),
     path('login/', loginView, name='login'),
     path('logout/', logoutView, name='logout'),
     path('questionsetting/', questionsettingView, name='setquestion'),
     path('questionsetsstudent/', questionsets_studentView, name='questionsetsstudent'),
     path('pensingstudentslist/', pendingStudentsListView, name='pendingstudents'),
     path('viewquestions/<str:group>/', viewQuestionsView, name='viewquestions'),
     path('answeringquestion/<str:group>/', answeringQuestionsView, name='answeringquestion'),
     path('resultteacher/', resultTeacherView, name='resultteacher'),
     path('resultstudent/', resultStudentView, name='resultstudent'),
    # path('signUpAdmin/', views.signUpAdmin, name='signUpAdmin'),

]