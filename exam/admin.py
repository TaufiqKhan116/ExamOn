from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(UserAbstract)
admin.site.register(Student)
admin.site.register(QuestionSetter)
admin.site.register(Admin)
admin.site.register(Question)
admin.site.register(TrueFalseQuestion)
admin.site.register(MCQQuestions)
admin.site.register(GroupAttr)
admin.site.register(StudentQuestionMap)