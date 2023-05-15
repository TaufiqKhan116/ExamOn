from django.contrib.auth import authenticate, login, logout
from django.http.response import  HttpResponseForbidden
from django.contrib.auth.hashers import make_password
from django.shortcuts import redirect, render
from .models import *


# Create your views here.

def IndexView(request) :
    '''Renders index page'''
    return render(request, 'index.html')

def AboutView(request) :
    '''Renders about page'''
    return render(request, 'about.html')

def ContactView(request) :
    '''Renders contact page'''
    return render(request, 'contact.html')

def resultTeacherView(request) :
    '''publishing results by teacher'''
    if request.method == 'POST' and request.POST['requesttype'] == 'publish' :
        groupAttrObj = GroupAttr.objects.get(group=request.POST['group'])
        groupAttrObj.isPublished = True
        groupAttrObj.save()
    elif request.method == 'POST' and request.POST['requesttype'] == 'unpublish' :
        groupAttrObj = GroupAttr.objects.get(group=request.POST['group'])
        groupAttrObj.isPublished = False
        groupAttrObj.save()

    if request.user.is_authenticated :
        group_list     = []
        isPublished    = {}
        setter         = QuestionSetter.objects.get(user=request.user)
        if setter.isVerified == True :
            question_set = Question.objects.filter(setter=setter).values('group').distinct()
            for i in range(len(question_set)) :
                group_list.append(question_set[i]['group'])
                isPublished[question_set[i]['group']] = GroupAttr.objects.get(group=question_set[i]['group']).isPublished
            context = {
                'is_published_list' : isPublished
            }
            return render(request, 'result_teacher.html', context)
        else :
            return render(request, 'index.html', { 'msg' : 'You are not verified yet. Please wait for a super user to verify.' })
    else:
        return redirect('exam:index')

def resultStudentView(request) :
    '''getting result by student'''
    if request.user.is_authenticated :
        markDict    = {}
        student     = Student.objects.get(user=request.user)
        mapObjSet   = StudentQuestionMap.objects.filter(student=student)

        for mapObj in mapObjSet :
            if not GroupAttr.objects.get(group=mapObj.question.group).isPublished :
                continue
            try :
                markDict[mapObj.question.group] = markDict[mapObj.question.group] + mapObj.question.marks
            except(KeyError) :
                markDict[mapObj.question.group] = 0
        
        context = {
                'result_dict' : markDict
            }

        return render(request, 'result_student.html', context)

def instructorSignUpView(request) :
    '''instructor sign up'''

    if request.method == "POST" :
        username        = request.POST['username']
        password        = request.POST['password']
        confirmPassword = request.POST['confirmpassword']
        email           = request.POST['email']
        hashed_password = make_password(password, salt=None, hasher='default')

        if password == confirmPassword :
            user    = UserAbstract.objects.create(
                username            = username,
                password            = hashed_password,
                isQuestionSetter    = True
            )
            instructor = QuestionSetter.objects.create(
                user    = user,
                name    = username,
                email   = email
            )
            instructor.save()
            login(request, user)
            return redirect('exam:index')

    return render(request, 'instructorSignUp.html')

def studentSignUpView(request) :
    '''student sign up'''

    if request.method == "POST" :
        username        = request.POST['username']
        password        = request.POST['password']
        confirmPassword = request.POST['confirmpassword']
        email           = request.POST['email']
        id              = request.POST['ID']
        hashed_password = make_password(password, salt=None, hasher='default')

        if password == confirmPassword :
            user = UserAbstract.objects.create(
                username    = username,
                password    = hashed_password,
                isStudent   = True
            )
            student = Student.objects.create(
                user        = user,
                name        = username,
                email       = email,
                studentID   = id
            )
            student.save()
            current_user = authenticate(
                username = username,
                password = password
            )
            login(request, user)
            return redirect('exam:index')

    return render(request, 'studentSignUp.html') 

def loginView(request) :
    '''log in'''

    if request.method == 'POST' :
        email       = request.POST['email']
        password    = request.POST['password']
        try :
            specific_user   = QuestionSetter.objects.get(email=email)
            user            = UserAbstract.objects.get(password=specific_user.user.password)
            auth_user       = authenticate(username=user.username, password=password)
            if auth_user is not None :
                login(request, auth_user)
        except QuestionSetter.DoesNotExist :
            try :
                specific_user   = Student.objects.get(email=email)
                user            = UserAbstract.objects.get(password=specific_user.user.password)
                auth_user       = authenticate(username=user.username, password=password)
                if auth_user is not None :
                    login(request, auth_user)
            except Student.DoesNotExist :
                redirect('exam:index')

    return redirect('exam:index')

def questionsets_studentView(request) :
    '''showing question-sets to student and receiving answer'''

    # submitting and storing student's answer
    if request.user.is_authenticated :
        if request.method == 'POST' and not request.POST.__contains__('passcode') :
            questionList =  [q.question for q in Question.objects.filter(group=request.POST['group'])]
            for question in questionList :
                queried_question = Question.objects.get(question=question)
                if queried_question.isTrueFalse and request.POST.__contains__(question) and str(TrueFalseQuestion.objects.get(question=queried_question).answer) == request.POST[question] :
                    StudentQuestionMap.objects.create(
                        question    = Question.objects.get(question=question),
                        student     = Student.objects.get(user=request.user)
                    ).save()
                elif queried_question.isMCQ and request.POST.__contains__(question) and int(MCQQuestions.objects.get(question=queried_question).answer) == int(request.POST[question]) :
                    StudentQuestionMap.objects.create(
                        question    = Question.objects.get(question=question),
                        student     = Student.objects.get(user=request.user)
                    ).save()

        # rendering question sets to student
        group_list  = []
        student     = Student.objects.get(user=request.user)
        if student.isVerified == True :
            question_set = Question.objects.all().values('group').distinct()
            for i in range(len(question_set)) :
                group_list.append(question_set[i]['group'])
            context = {
                'q_group_list' : group_list,
            }
            return render(request, 'questionsets_student.html', context)
        else :
            return render(request, 'index.html', { 'msg' : 'You are not verified yet. Please wait for a super user or a teacher to verify.' })
    
    else:
        return redirect('exam:index')

def pendingStudentsListView(request) :
    '''handles pending verification request of students'''

    if request.method == 'POST' and request.is_ajax() and request.POST['requesttype'] == 'pendinglistupdate':
        ID                  = request.POST['ID']
        student             = Student.objects.get(studentID=ID)
        student.isVerified  = True
        student.save()

    if request.user.is_authenticated :
        student_list = []
        setter = QuestionSetter.objects.get(user=request.user)
        if setter.isVerified == True :
            student_set = Student.objects.filter(isVerified=False).distinct()
            for i in range(len(student_set)) :
                student_list.append(student_set[i])
            context = {
                'student_list' : student_list,
            }
            return render(request, 'pendingstudentlist.html', context)
        else :
            return render(request, 'index.html', { 'msg' : 'You are not verified yet. Please wait for a super user to verify.' })
    else:
        return redirect('exam:index')

def questionsettingView(request) :
    '''showing question-sets by individual instructor'''

    if request.method == 'POST' :
        instructor      = QuestionSetter.objects.get(user=request.user)
        questionGroup   = ''
        question        = request.POST['question']
        marks           = request.POST['marks']
        isTrueFalse     = False
        isMCQ           = False
        isFile          = False
        question_obj    = None
        tfanswer        = False

        if 'isNewQuestionSet' in request.POST and request.POST['isNewQuestionSet'] == 'on' :
            questionGroup  = request.POST['newQuestionSet']
            groupAttrObj   = GroupAttr.objects.create(
                group       = questionGroup,
                elapsedTime = 0,
                passcode    = ''
            )
        else :
            questionGroup = request.POST['existingQuestionSet']

        if request.POST['typeOfQuestion'] == 'tf' :
            isTrueFalse = True
            tfanswer    = True if request.POST['answer_tf'] == 'true' else False
        elif request.POST['typeOfQuestion'] == 'mcq' :
            isMCQ       = True
        else:
            isFile      = True

        question_obj = Question.objects.create(
            setter      = instructor,
            group       = questionGroup,
            question    = question,
            marks       = marks,
            isTrueFalse = isTrueFalse,
            isMCQ       = isMCQ,
            isFile      = isFile
        )

        if isTrueFalse :
            TrueFalseQuestion.objects.create(
                question    = question_obj,
                answer      = tfanswer
            ).save()
            question_obj.save()

        if isMCQ :
            MCQQuestions.objects.create(
                question    = question_obj,
                opt_1       = request.POST['mcq_option_1'],
                opt_2       = request.POST['mcq_option_2'],
                opt_3       = request.POST['mcq_option_3'],
                opt_4       = request.POST['mcq_option_4'],
                answer      = request.POST['mcq_answer'],
            ).save()
            question_obj.save()
        
        if isFile :
            question_obj.save()

    if request.user.is_authenticated :
        group_list  = []
        setter      = QuestionSetter.objects.get(user=request.user)
        if setter.isVerified == True :
            question_set = Question.objects.filter(setter=setter).values('group').distinct()
            for i in range(len(question_set)) :
                group_list.append(question_set[i]['group'])
            context = {
                'q_group_list' : group_list,
            }
            return render(request, 'questionsetting.html', context)
        else :
            return render(request, 'index.html', { 'msg' : 'You are not verified yet. Please wait for a super user to verify.' })
    else:
        return redirect('exam:index')

def answeringQuestionsView(request, group) :
    '''checking passcode and rendering questions'''

    if request.method == 'POST' and request.POST.__contains__('passcode') and request.POST['requesttype'] == 'passcodecheck' :
        if GroupAttr.objects.get(group=group).passcode == request.POST['passcode'] :
            context     = {}
            itr         = 0
            questions   = Question.objects.filter(group=group)
            try :
                elapsedtime = GroupAttr.objects.get(group=group).elapsedTime if GroupAttr.objects.get(group=group).elapsedTime != None else 0
            except :
                elapsedtime = 0

            context['group']        = group
            context['elapsedtime']  = str(elapsedtime)
            for question in questions :
                if question.isTrueFalse :
                    context[str(itr)] = {
                        'type'      : 'tf',
                        'question'  : question.question,
                    }
                elif question.isMCQ :
                    mcq = MCQQuestions.objects.get(question=question)
                    context[str(itr)] = {
                        'type'      : 'mcq',
                        'question'  : question.question,
                        'opt1'      : mcq.opt_1,
                        'opt2'      : mcq.opt_2,
                        'opt3'      : mcq.opt_3,
                        'opt4'      : mcq.opt_4,
                    }
                elif question.isFile :
                    context[str(itr)] = {
                        'type'      : 'f',
                        'question'  : question.question,
                    }
                itr +=1
            return render(request, 'answeringquestion.html', { 'mycontext' : context})
        else :
            return HttpResponseForbidden

    # elif request.method == 'POST' and not request.POST.__contains__('passcode'):
    #     questionList =  [q.question for q in Question.objects.filter(group=group)]
    #     for question in questionList :
    #         queried_question = Question.objects.get(question=question)
    #         if queried_question.isTrueFalse  and str(TrueFalseQuestion.objects.get(question=queried_question).answer) == request.POST[question] :
    #             StudentQuestionMap.objects.create(
    #                 question    = Question.objects.get(question=question),
    #                 student     = Student.objects.get(user=request.user)
    #             ).save()
    #         elif queried_question.isMCQ and int(MCQQuestions.objects.get(question=queried_question).answer) == int(request.POST[question]) :
    #             StudentQuestionMap.objects.create(
    #                 question    = Question.objects.get(question=question),
    #                 student     = Student.objects.get(user=request.user)
    #             ).save()
        

def viewQuestionsView(request, group) :
    '''rendering questions to instructor'''

    if request.method == 'POST' and request.is_ajax() and request.POST['questiontype'] == 'none' and request.POST['requesttype'] == 'passcodeupdate':
        targetgroup             = request.POST['group']
        newpasscode             = request.POST['passcode']
        groupAttrObj            = GroupAttr.objects.get(group=targetgroup)
        groupAttrObj.passcode   = newpasscode
        groupAttrObj.save()

    if request.method == 'POST' and request.is_ajax() and request.POST['questiontype'] == 'none' and request.POST['requesttype'] == 'timeupdate':
        targetgroup                 = request.POST['group']
        newelapsedtime              = request.POST['elapsedtime']
        groupAttrObj                = GroupAttr.objects.get(group=targetgroup)
        groupAttrObj.elapsedTime    = float(newelapsedtime) if newelapsedtime != '' else 0
        groupAttrObj.save()

    if request.method == 'POST' and request.is_ajax() and request.POST['questiontype'] == 'tf' and request.POST['requesttype'] == 'update':
        previousQuestion    = request.POST['previousquestion']
        newQuestion         = request.POST['newquestion']
        answer              =  request.POST['newanswer']
        questionSetter      = QuestionSetter.objects.get(user=request.user)
        question            = Question.objects.get(group=group, question=previousQuestion)
        answerObj           = TrueFalseQuestion.objects.get(question=question)
        question.question   = newQuestion
        answerObj.answer    = True if answer == 'True' else False
        question.save()
        answerObj.save()

    if request.method == 'POST' and request.is_ajax() and request.POST['questiontype'] == 'tf' and request.POST['requesttype'] == 'delete':
        previousQuestion    = request.POST['question']
        questionSetter      = QuestionSetter.objects.get(user=request.user)
        question            = Question.objects.get(group=group, question=previousQuestion)
        question.delete()
        if Question.objects.count() - 1 <= 0 :
            GroupAttr.objects.get(group=group).delete()

    if request.method == 'POST' and request.is_ajax() and request.POST['questiontype'] == 'mcq' and request.POST['requesttype'] == 'update':
        previousQuestion    = request.POST['previousquestion']
        newQuestion         = request.POST['newquestion']
        nopt1               = request.POST['nopt1']
        nopt2               = request.POST['nopt2']
        nopt3               = request.POST['nopt3']
        nopt4               = request.POST['nopt4']
        answer              =  request.POST['newanswer']
        questionSetter      = QuestionSetter.objects.get(user=request.user)
        question            = Question.objects.get(group=group, question=previousQuestion)
        answerObj           = MCQQuestions.objects.get(question=question)
        question.question   = newQuestion
        answerObj.opt_1     = nopt1
        answerObj.opt_2     = nopt2
        answerObj.opt_3     = nopt3
        answerObj.opt_4     = nopt4
        answerObj.answer    = answer
        question.save()
        answerObj.save()

    if request.method == 'POST' and request.is_ajax() and request.POST['questiontype'] == 'mcq' and request.POST['requesttype'] == 'delete':
        previousQuestion    = request.POST['question']
        questionSetter      = QuestionSetter.objects.get(user=request.user)
        question            = Question.objects.get(group=group, question=previousQuestion)
        question.delete()
        if Question.objects.count() - 1 <= 0 :
            GroupAttr.objects.get(group=group).delete()

    context         = {}
    itr             = 0
    passcode        = ''
    elapsedtime     = 0
    questionSetter  = QuestionSetter.objects.get(user=request.user)
    questions       = Question.objects.filter(setter=questionSetter, group=group)
    try :
        elapsedtime = GroupAttr.objects.get(group=group).elapsedTime if GroupAttr.objects.get(group=group).elapsedTime != None else 0
        passcode    = GroupAttr.objects.get(group=group).passcode if GroupAttr.objects.get(group=group).elapsedTime != None else ''
    except :
        elapsedtime = 0
        passcode    = ''

    context['group']        = group
    context['elapsedtime']  = str(elapsedtime)
    context['passcode']     = passcode
    for question in questions :
        if question.isTrueFalse :
            tfq = TrueFalseQuestion.objects.get(question=question)
            context[str(itr)] = {
                'type'      : 'tf',
                'question'  : question.question,
                'answer'    : tfq.answer
            }
        elif question.isMCQ :
            mcq = MCQQuestions.objects.get(question=question)
            context[str(itr)] = {
                'type'      : 'mcq',
                'question'  : question.question,
                'opt1'      : mcq.opt_1,
                'opt2'      : mcq.opt_2,
                'opt3'      : mcq.opt_3,
                'opt4'      : mcq.opt_4,
                'answer'    : mcq.answer
            }
        elif question.isFile :
            context[str(itr)] = {
                'type'      : 'f',
                'question'  : question.question,
            }
        itr +=1
    return render(request, 'viewquestions.html', { 'mycontext' : context})

def logoutView(request) :
    '''log out'''
    logout(request)
    return redirect('exam:index')