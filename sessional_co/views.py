from django.shortcuts import render, redirect
from django.contrib import messages
from core.models import Subject, CourseOutcome
from .models import SessionalTable

def sessional_list(request):
    if request.method == "POST":
        subject = Subject.objects.filter(uuid=request.POST['subject_uuid']).first()
        student_list = request.POST['student_list'].split('\r\n')
        student_json = {}
        for student in student_list:
            temp_student = student.split('\t')
            student_json[temp_student[0]] = temp_student[1]
        
        cos = CourseOutcome.objects.filter(subject=subject)
        co_json = {}
        for co in cos:
            co_json[f"CO{co.number}"] = {}
            for student in student_json.keys():
                co_json[f"CO{co.number}"][student] = ''
        
        try:
            sessional = SessionalTable.objects.create(faculty=request.user,
                session=request.POST['session'], semester=request.POST['semester'], student_info=student_json, subject=subject,
                ct1=co_json, ct2=co_json, put=co_json, assignment_tutorial=co_json)
            messages.info(request, 'Table Created')
        except:
            print()
        
    subjects = Subject.objects.all()
    sessionals = SessionalTable.objects.filter(faculty=request.user)
    context = {
        'subjects': subjects,
        'sessionals': sessionals
    }
    return render(request, 'sessional-list.html', context)

def sessional_table_edit(request, pk, field):
    table = SessionalTable.objects.filter(uuid=pk).first()
    if field == 'ct1':
        table_dict = table.ct1
    elif field == 'ct2':
        table_dict = table.ct2
    elif field == 'put':
        table_dict = table.put
    elif field == 'assignment_tutorial':
        table_dict = table.assignment_tutorial

    table_header = table_dict.keys()

    table_body = {}
    for key, value in table_dict.items():
        for k, v in value.items():
            try:
                table_body[k].append(v)
            except:
                table_body[k] = [v]
    context = {
        'table_header': table_header,
        'table_body': table_body,
        'field': field,
    }

    if request.method == "POST":
        table = SessionalTable.objects.filter(uuid=pk).first()
        if field == 'ct1':
            table_dict = table.ct1
        elif field == 'ct2':
            table_dict = table.ct2
        elif field == 'put':
            table_dict = table.put
        elif field == 'assignment_tutorial':
            table_dict = table.assignment_tutorial
        
        for key, value in table_dict.items():
            for v in value.keys():
                table_dict[key][v] = request.POST[f'{key}_{v}']
        
        table.save()
        return redirect('sessional-table-edit', pk=pk, field=field)
    
    return render(request, 'sessional-table-edit.html', context)

