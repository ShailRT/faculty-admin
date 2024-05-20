from django.shortcuts import render, redirect
from django.utils.text import slugify
from .forms import SessionStudentCreateForm, CreateStudentInfoForm, ExitSurveyCreateForm
from django.contrib import messages
from .models import ExitSurvey, StudentInfo, SessionStudent
from core.models import Subject, CourseOutcome


department_choices = ( ('IT', 'IT' ), ('CS', 'CS'), ('AI/ML', 'AI/ML'), ('IOT', 'IOT'))
program_choices = ( ('B.Tech', 'B.Tech' ),)

def exit_survey_form(request, pk):
    survey = ExitSurvey.objects.filter(slug=pk).first()
    cos = CourseOutcome.objects.filter(subject=survey.subject)
    if request.method == "POST":
        co_res = {}
        for co in cos:
            co_res[f'CO{co.number}'] = request.POST[f'co{co.number}']
        student = StudentInfo.objects.filter(university_roll_no=request.POST['uni-rollno']).first()
        student.co_response[survey.subject.code] = co_res
        student.save()
        messages.info(request, 'Form Submitted Successfuly')
        return redirect('exit-survey-form', pk=pk)
    context = {
        'survey': survey,
        'cos': cos
    }
    return render(request, 'base-form.html', context)

def exit_survey(request):
    if request.method == "POST":
        form = ExitSurveyCreateForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.faculty = request.user
            temp_res = {}
            temp_res[form.subject.code] = {}
            cos = CourseOutcome.objects.filter(subject=form.subject)
            for co in cos:
                temp_res[form.subject.code][f'CO{co.number}'] = 0
            for student in form.session.students.all():
                stu = StudentInfo.objects.filter(university_roll_no=student.university_roll_no).first()
                stu.co_response = temp_res
                stu.save()
            form.save()
        else:
            print(form.errors)
        return redirect('exit-survey')
        
    form = ExitSurveyCreateForm()
    subjects = Subject.objects.all()
    sessions = SessionStudent.objects.filter(department=request.user.department)
    surveys = ExitSurvey.objects.filter(faculty=request.user)

    context = {
        'subjects': subjects,
        'surveys': surveys,
        'sessions': sessions,
        'department_choices': department_choices,
        'form': form,
    }
    return render(request, 'exit-survey.html', context)

def survey_student_list(request, pk):
    survey = ExitSurvey.objects.filter(id=pk).first()
    cos = CourseOutcome.objects.filter(subject=survey.subject)
    
    
    context = {
        'survey': survey,
        'cos': cos,
    }

    return render(request, 'survey-student-list.html', context)

def session_list(request):
    if request.method == "POST":
        print(request.POST)
        form = SessionStudentCreateForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.faculty = request.user
            form.save()
            messages.info(request, 'Session Student List Created Successfully')
        else:
            print(form.errors)
        return redirect('session-list')
    session_list = SessionStudent.objects.filter(faculty=request.user)
    form = SessionStudentCreateForm()
    context = {
        'session_list': session_list,
        'form': form,
        'department_choices': department_choices,
        'program_choices': program_choices,
    }
    return render(request, 'student/student-list.html', context)

def view_student(request, pk):
    session = SessionStudent.objects.filter(uuid=pk).first()
    if request.method == "POST":
        form = CreateStudentInfoForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.save()
            student = StudentInfo.objects.filter(university_roll_no=form.cleaned_data['university_roll_no']).first()
            session.students.add(student)
            messages.info(request, 'Student added')
        else:
            print(form.errors)
        return redirect("view-student", pk=pk)
    
    context = {
        "session": session,
    }
    
    return render(request, "student/add-student.html", context)
    


