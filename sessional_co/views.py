from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from core.models import Subject, CourseOutcome, AccessRequest
from .models import SessionalTable
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
import pandas as pd
import json
from datetime import datetime
from .helpers import save_pdf 
from django.http import FileResponse
from django.conf import settings
import os

from xhtml2pdf import pisa
from django.template.loader import get_template


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
        max_marks = {}
        for co in cos:
            max_marks[f'CO{co.number}'] = {
                'ct1': 0, 
                'ct2': 0, 
                'put': 0, 
                'ant': 0, 
            }
            co_json[f"CO{co.number}"] = {}
            for student in student_json.keys():
                co_json[f"CO{co.number}"][student] = ''
        
        try:
            sessional = SessionalTable.objects.create(faculty=request.user,
                session=request.POST['session'], semester=request.POST['semester'], student_info=student_json, subject=subject,
                ct1=co_json, ct2=co_json, put=co_json, assignment_tutorial=co_json, max_marks=max_marks)
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
    subject = table.subject
    if field == 'ct1':
        table_dict = table.ct1
    elif field == 'ct2':
        table_dict = table.ct2
    elif field == 'put':
        table_dict = table.put
    elif field == 'ant':
        table_dict = table.assignment_tutorial

    table_header = table_dict.keys()

    table_body = {}
    for key, value in table_dict.items():
        for k, v in value.items():
            try:
                table_body[k].append(v)
            except:
                table_body[k] = [v]
    max_marks = {}
    for key, value in table.max_marks.items():
        max_marks[key] =  value[field] 
    
    context = {
        'table_header': table_header,
        'table_body': table_body,
        'field': field,
        'subject': subject,
        'table_uuid': table.uuid,
        'max_marks': max_marks,
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
        
        for key in table.max_marks.keys():
            table.max_marks[key][field] = int(request.POST[f'{key}_maxmarks'])
        try:
            table.save()
            messages.info(request, 'Table Updated!')
        except Exception as e: 
            print(e)
        return redirect('sessional-table-edit', pk=pk, field=field)
    
    return render(request, 'sessional-table-edit.html', context)


def test_pdf(request, pk):
    sessional = SessionalTable.objects.filter(uuid=pk).first()
    cos = CourseOutcome.objects.filter(subject=sessional.subject)
    data = {}
    for no in sessional.student_info.keys():
        data[no] = {}
    
    for key, value in sessional.ct1.items():
        for k, v in value.items():
            try:
                data[k][key]['ct1'] = v
            except KeyError:
                data[k][key] = {}
                data[k][key]['ct1'] = v
    
    for key, value in sessional.ct2.items():
        for k, v in value.items():
            try:
                data[k][key]['ct2'] = v
            except KeyError:
                data[k][key] = {}
                data[k][key]['ct2'] = v

    for key, value in sessional.put.items():
        for k, v in value.items():
            try:
                data[k][key]['put'] = v
            except KeyError:
                data[k][key] = {}
                data[k][key]['put'] = v
    
    for key, value in sessional.assignment_tutorial.items():
        for k, v in value.items():
            try:
                data[k][key]['a/t'] = v
            except KeyError:
                data[k][key] = {}
                data[k][key]['a/t'] = v

    max_marks = {}
    for key, value in sessional.max_marks.items():
        max_marks[key] = sum(value.values())
    for key, value in data.items():
        for ke, val in value.items():
            total = 0
            for k, v in val.items():
                if v!='':
                    total+=int(v)
                else:
                    total+=0
            if total == 0 or max_marks[ke] == 0:
                value[ke]['percentage'] = 0
            else:
                value[ke]['percentage'] = round((total/max_marks[ke])*100, 2)
            
    params = {
        'cos': cos,
        'data': data,
        'table_session': sessional.session, 
        'table_semester': sessional.semester,
        'table_odd_or_even': 'Odd' if int(sessional.semester[0])%2==1 else 'Even',
        'table_faculty_name': sessional.faculty.first_name+' '+sessional.faculty.last_name,
        'table_subject': sessional.subject,
        'table_department': sessional.faculty.department,

    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f"filename='{sessional.subject.title}-{sessional.semester}.pdf'"

    template = get_template('pdf.html')

    html = template.render(params)

    pisa_status = pisa.CreatePDF(
       html, dest=response)
    
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def sessional_table_edit_request(request):
    if not AccessRequest.objects.filter(message='SESSIONAL_TABLE_EDIT_ACCESS', user=request.user).exists():
        AccessRequest.objects.create(message='SESSIONAL_TABLE_EDIT_ACCESS', user=request.user)
        messages.info(request, 'Your request is sent!')
    else:
        messages.info(request, 'Your request already exists!')

    table_uuid = request.GET.get('table_uuid')
    field = request.GET.get('field')
    
    
    return redirect(f'/sessional-table/{table_uuid}/{field}')
