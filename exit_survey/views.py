from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.text import slugify
from .forms import SessionStudentCreateForm, CreateStudentInfoForm, ExitSurveyCreateForm
from django.contrib import messages
from .models import ExitSurvey, StudentInfo, SessionStudent
from core.models import Subject, CourseOutcome
from sessional_co.models import SessionalTable
import csv


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
        if StudentInfo.objects.filter(university_roll_no=request.POST['uni-rollno']).exists():
            student.co_response[survey.subject.code] = co_res
            student.save()
            messages.info(request, 'Form Submitted Successfuly')
        else:
            messages.info(request, "You are not registered as a student please contact your mentor.")
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
                stu.co_response.update(temp_res)
                stu.save()
            form.save()
        else:
            print(form.errors)
        return redirect('exit-survey')
        
    form = ExitSurveyCreateForm()
    subjects = request.user.subjects.all()
    sessions = SessionStudent.objects.filter(department=request.user.department, faculty=request.user)
    surveys = ExitSurvey.objects.filter(faculty=request.user)
    if request.user.is_admin:
        surveys = ExitSurvey.objects.all()

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
    attainment = {}
    for co in cos:
        attainment[f'CO{co.number}'] = {
            'count': 0,
            'percentage': 0.0,
            'level': 0
            }
        
    for student in survey.session.students.all():
        for key, value in student.co_response[survey.subject.code].items():
            if int(value) >= 3:
                attainment[key]['count'] += 1
    total_students = len(survey.session.students.all())  
    for value in attainment.values():
        value['percentage'] = (value['count']/total_students)*100
        if value['percentage'] < 50:
            value['level'] = 1
        elif value['percentage'] < 60:
            value['level'] = 2
        else:
            value['level'] = 3
    
    
    context = {
        'survey': survey,
        'cos': cos,
        'attainment': attainment,
    }

    return render(request, 'survey-student-list.html', context)

def session_list(request):
    if request.method == "POST":
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
    if request.user.is_admin:
        session_list = SessionStudent.objects.all()
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
        student = StudentInfo.objects.filter(university_roll_no=request.POST['university_roll_no'])
        form = CreateStudentInfoForm(request.POST)
        if form.is_valid():
            print("form data /n", form.data)
            form = form.save(commit=False)
            co_response, final_marks = {}, {}

            if len(session.students.all()) > 0:
                latest_student = session.students.all()[0]
                co_response = latest_student.co_response
                for key, value in co_response.items():
                    for ke in value.keys():
                        co_response[key][ke] = 0
                final_marks = latest_student.final_marks
                for key in final_marks.keys():
                    final_marks[key]['scored'] = 0
            
            form.co_response, form.final_marks = co_response, final_marks
            form.save() 
            student = StudentInfo.objects.filter(university_roll_no=request.POST['university_roll_no']).first()
            session.students.add(student)
            session.save()
            tables = SessionalTable.objects.filter(session=session)
            for table in tables:
                for key in table.ct1.keys():
                    table.ct1[key][student.university_roll_no] = ""
                for key in table.ct2.keys():
                    table.ct2[key][student.university_roll_no] = ""
                for key in table.put.keys():
                    table.put[key][student.university_roll_no] = ""
                for key in table.assignment_tutorial.keys():
                    table.assignment_tutorial[key][student.university_roll_no] = ""
                table.save()
            
            messages.info(request, 'Student added')

        elif len(student)>0 and student.first() not in session.students.all():
            student = StudentInfo.objects.filter(university_roll_no=request.POST['university_roll_no']).first()
            session.students.add(student)
            session.save()
            tables = SessionalTable.objects.filter(session=session)
            for table in tables:
                for key in table.ct1.keys():
                    table.ct1[key][student.university_roll_no] = ""
                for key in table.ct2.keys():
                    table.ct2[key][student.university_roll_no] = ""
                for key in table.put.keys():
                    table.put[key][student.university_roll_no] = ""
                for key in table.assignment_tutorial.keys():
                    table.assignment_tutorial[key][student.university_roll_no] = ""
                print('table', table.ct1)
                table.save()
        else:
            messages.info(request, form.errors)
            print(form.errors)
        return redirect("view-student", pk=pk)
    
    context = {
        "session": session,
    }
    
    return render(request, "student/add-student.html", context)

def final_subjects(request, pk):
    session = SessionStudent.objects.filter(uuid=pk).first()
    if request.method == "POST":
        subject = Subject.objects.filter(uuid=request.POST['subject_uuid']).first()
        for student in session.students.all():
            if subject.code not in student.final_marks.keys():
                student.final_marks[subject.code] = {'scored': 0, 'max-marks': 0}
                student.save()
            else:
                messages.info(request, f'{student.university_roll_no} Subject Already Present')
        session.final_subjects.add(subject)
        session.save()
        messages.info(request, 'Subject Added')
        return redirect('final-subjects', pk=pk)
        
    subjects = request.user.subjects.all()
    context = {
        'session': session,
        'subjects': subjects,
        'final_subjects': session.final_subjects.all(),
    }
    return render(request, 'final-marks/add-subject.html', context)

def final_marks(request, pk, sub):
    session = SessionStudent.objects.filter(uuid=pk).first()
    subject = Subject.objects.filter(uuid=sub).first()

    if request.method == "POST":
        for student in session.students.all():
            if subject.code in student.final_marks.keys():
                student.final_marks[subject.code]['max-marks'] = request.POST['max-marks']
                student.final_marks[subject.code]['scored'] = request.POST[student.university_roll_no]
                student.save()
        messages.info(request, 'final marks updated')
        return redirect('final-marks', pk=pk, sub=sub)
    
    data = {'student':{}, 'max_marks': 0}
    for student in session.students.all():
        if subject.code in student.final_marks.keys():
            data['student'][student.university_roll_no] = float(student.final_marks[subject.code]['scored'])
            if data['max_marks'] == 0:
                data['max_marks'] = float(student.final_marks[subject.code]['max-marks'])
        else:
            messages.error(request, f'{student.university_roll_no} subject not present')
    
    co_attainment = {
        'count': 0,
        'percentage': 0.0,
        'level': 0,
    }        
    for value in data['student'].values():
        if data['max_marks']!=0 and value/data['max_marks'] >= 0.5:
            co_attainment['count']+=1
        
    co_attainment['percentage'] = (co_attainment['count']/len(data['student']))*100
    if co_attainment['percentage'] < 50.0:
        co_attainment['level'] = 1
    elif co_attainment['percentage'] < 60:
        co_attainment['level'] = 2
    else:
        co_attainment['level'] = 3
        
    context = {
        'session': session,
        'subject': subject,
        'data': data,
        'co_attainment': co_attainment,
    }
    
    return render(request, 'final-marks/final-marks.html', context)

    


def student_csv(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        
        # Ensure the file is a CSV
        if not csv_file.name.endswith('.csv'):
            return HttpResponse("Please upload a CSV file.")
        
        # Decode the file
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.reader(decoded_file) 

        # Iterate over the rows in the CSV file and create Product instances
        session = SessionStudent.objects.filter(uuid=request.POST['session']).first()

        try:
            stu_count = 0
            for row in reader:
                stu_count+=1
                university_roll_no, admission_roll_no, first_name, last_name = row
                student = StudentInfo.objects.filter(university_roll_no=university_roll_no)
                if len(student)>0 and student.first() not in session.students.all():
                    session.students.add(student.first())
                    session.save()
                else:
                    StudentInfo.objects.create(university_roll_no=university_roll_no, admission_roll_no=admission_roll_no,  first_name=first_name, last_name=last_name)
                    new_student = StudentInfo.objects.filter(university_roll_no=university_roll_no).first()
                    session = SessionStudent.objects.filter(uuid=request.POST['session']).first()
                    session.students.add(new_student)
                    session.save()
            messages.info(request, f'{stu_count} student added')
        except Exception as e:
            print("upload student failed with ", e)
            messages.info(request, e)


        return redirect("view-student", pk=session.uuid)
    sessions = SessionStudent.objects.all()
    return render(request, "student-upload.html", {'sessions': sessions})
