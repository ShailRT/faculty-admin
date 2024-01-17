from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from .forms import CustomUserForm, ProgramOutcomeForm
from .models import Subject, CourseOutcome, ProgramOutcome, ProgramEducationalObjective, ProgramSpecificOutcome, FacultyInfo, College, AccessRequest
import json
import csv

department_choices = ('IT','CS','AI/ML','IOT')
college_choices = ('GNIOT', 'GIMS')


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_login_permitted:
                auth_login(request, user)
                return redirect('dashboard')
            else:
                messages.info(request, 'Your account is not yet permitted')
                return redirect('login')
        else:
            return redirect('login')
    else:
        return render(request, 'registration/login.html')

def registration(request):
    if request.method == "POST":
        form = CustomUserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.info(request, "Wait for approval")
            return redirect('login')
        else: 
            errors = form.errors 
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return redirect('register')
    else:
        form = CustomUserForm()
        facultys = FacultyInfo.objects.all()
        selected_faculty = None
        college = None
        selected_faculty_id = request.GET.get('selected_faculty_id')
        if selected_faculty_id:
            selected_faculty = FacultyInfo.objects.filter(id=selected_faculty_id).first()
            college = College.objects.filter(title=selected_faculty.college_name).first()
        context = {
            'form': form,
            'title': 'Registration',
            'facultys': facultys,
            'selected_faculty': selected_faculty,
            'college': college
        }

        return render(request, 'registration/register.html', context)

@login_required(login_url='login')
def index(request):
    user = request.user

    context = {
        'user': user
    }
    return render(request, 'index.html', context)

@login_required(login_url='login')
def add_subject(request):
    if request.method == "POST":
        subject = Subject.objects.filter(uuid=request.POST['subject_uuid']).first()
        user = request.user
        user.subjects.add(subject)
        user.save()
        messages.info(request, f"Subject Added {subject.title}")
        return redirect('add-subject')
        
    subjects = Subject.objects.all()
    user_subjects = request.user.subjects.all()
    context = {
        'subjects': subjects,
        'user_subjects': user_subjects
    }
    return render(request, 'subject/add-subject.html', context)

@login_required(login_url='login')
def remove_subject(request, pk):
    subject_uuid = pk 
    subject = Subject.objects.filter(uuid=subject_uuid).first()
    user = request.user
    user.subjects.remove(subject)
    user.save()
    messages.info(request, f'Subject removed {subject.title}')

    return redirect('add-subject')

@login_required(login_url='login')
def co_po_table(request):
    if request.method == "POST":
        subject_uuid = request.POST['subject_uuid']
        selected_department = request.POST['selected_department']
        subject = Subject.objects.filter(uuid=subject_uuid).first()
        co_list = CourseOutcome.objects.filter(subject=subject)
        for co in co_list:
            for po in co.program_outcome_priority.keys():
                co.program_outcome_priority[po] = request.POST[f'CO{co.number}_{po}']
            for pso in co.program_specific_outcome_priority[selected_department].keys():
                co.program_specific_outcome_priority[selected_department][pso] = request.POST[f'CO{co.number}_{pso}']
            for peo in co.program_educational_objective_priority[selected_department].keys():
                co.program_educational_objective_priority[selected_department][peo] = request.POST[f'CO{co.number}_{peo}']
            co.save()
        messages.info(request, "Table Saved")
        return redirect(f'/co-po-table?subject_uuid={subject_uuid}&selected_department={selected_department}')
    else:
        subjects = request.user.subjects.all()
        selected_subject = None
        departments =  department_choices
        selected_department = request.GET.get('selected_department')
        selected_subject_uuid = request.GET.get('subject_uuid')
        co_po_header = []
        co_list = {}
        co_render_list = {}
        if selected_subject_uuid != '' and selected_subject_uuid != None and selected_department != '' and selected_department != None:
            selected_subject = Subject.objects.filter(uuid=selected_subject_uuid).first()
            
            co_list = CourseOutcome.objects.filter(subject=selected_subject)
            if len(co_list) > 0:
                co_po_header = list(co_list.first().program_outcome_priority.keys()) + list(co_list.first().program_specific_outcome_priority[selected_department].keys()) + list(co_list.first().program_educational_objective_priority[selected_department].keys())
                for co in co_list:
                    co_render_list[f"CO{co.number}"] = {
                        'PO': list(co.program_outcome_priority.values()),
                        'PSO': list(co.program_specific_outcome_priority[selected_department].values()),
                        'PEO': list(co.program_educational_objective_priority[selected_department].values())
                    }
        
        context = {
            'co_render_list': co_render_list,
            "co_po_header": co_po_header,
            "subjects": subjects,
            'departments': departments,
            'selected_subject' : selected_subject,
            'selected_department' : selected_department,
        }
        return render(request, 'co-po/co-po-table.html', context)
    
@login_required(login_url='login')
def add_co(request):
    subject_uuid = request.GET.get('subject_uuid')
    selected_department = request.GET.get('selected_department')
    selected_subject = Subject.objects.filter(uuid=subject_uuid).first()

    if request.method == "POST":
        pos = ProgramOutcome.objects.filter(program=selected_subject.program)
        
        program_outcome_priority = {}
        program_educational_objective_priority = {}
        program_specific_outcome_priority = {}
        for dep in department_choices:
            program_specific_outcome_priority[dep] = {}
            program_educational_objective_priority[dep] = {}
        
        for po in pos:
            program_outcome_priority[f'PO{po.number}'] = None

        
        for dep in department_choices:
            psos = ProgramSpecificOutcome.objects.filter(department=dep, program=selected_subject.program)
            for pso in psos:
                program_specific_outcome_priority[f"{dep}"][f'PSO{pso.number}'] = None
            
            peos = ProgramEducationalObjective.objects.filter(department=dep, program=selected_subject.program)
            for peo in peos:
                program_educational_objective_priority[f"{dep}"][f'PEO{peo.number}'] = None
        
        CourseOutcome.objects.create(number=request.POST['number'], message=request.POST['message'], subject=selected_subject, program_outcome_priority=program_outcome_priority, program_educational_objective_priority=program_educational_objective_priority, program_specific_outcome_priority=program_specific_outcome_priority)
        return redirect(f'/add-co?subject_uuid={selected_subject.uuid}')
        

    subject_cos = []
    if selected_subject != '' and selected_subject != None:
        subject_cos = CourseOutcome.objects.filter(subject=selected_subject)
    
    subjects = request.user.subjects.all() 
    context = {
        'subjects': subjects,
        'subject_cos': subject_cos,
        'selected_subject': selected_subject,
    }
    return render(request, 'co-po/add-co.html', context)

def add_po(request):
    selected_program = request.GET.get('selected_program')
    
    if request.method == "POST":
        form = ProgramOutcomeForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(f'/add-po?selected_program={selected_program}')

    pos = ProgramOutcome.objects.all()
    selected_pos = []
    if selected_program != '' and selected_program != None:
        selected_pos = ProgramOutcome.objects.filter(program=selected_program) 
    programs = []
    for po in pos:
        if po.program not in programs:
            programs.append(po.program)

    form = ProgramOutcomeForm()        
    context = {
        'programs': programs,
        'selected_program': selected_program,
        'selected_pos': selected_pos,
        'form': form,
    }

    return render(request, 'co-po/add-po.html', context)

def download_table(request, pk):
    subject = Subject.objects.filter(uuid=pk).first()
    selected_department = request.GET.get('selected_department')
    cos = CourseOutcome.objects.filter(subject=subject)

    csv_file_name = f'table-{subject.title}'

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{csv_file_name}.csv"'

    csv_writer = csv.writer(response)

    csv_writer.writerow(list(cos.first().program_outcome_priority.keys())+list(cos.first().program_specific_outcome_priority[selected_department].keys())+list(cos.first().program_educational_objective_priority[selected_department].keys()))
    for co in cos:
        csv_writer.writerow(list(co.program_outcome_priority.values())+list(co.program_specific_outcome_priority[selected_department].values())+list(co.program_educational_objective_priority[selected_department].values()))
    
    return response

def delete_co(request, pk):
    co = CourseOutcome.objects.filter(uuid=pk).first()
    co.delete()
    subject_uuid = request.GET.get('subject_uuid')
    return redirect(f'/add-co?subject_uuid={subject_uuid}')

def table_edit_request(request):
    if not AccessRequest.objects.filter(message='TABLE_EDIT_ACCESS', user=request.user).exists():
        AccessRequest.objects.create(message='TABLE_EDIT_ACCESS', user=request.user)
        messages.info(request, 'Your request is sent!')
    else:
        messages.info(request, 'Your request already exists!')

    subject_uuid = request.GET.get('subject_uuid')
    selected_department = request.GET.get('selected_department')
    
    return redirect(f'/co-po-table?subject_uuid={subject_uuid}&selected_department={selected_department}')
            