from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from core.models import Subject, CourseOutcome
from .models import SessionalTable
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
import pandas as pd
import json
from datetime import datetime 

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

def sessional_table_download(request, pk):
    sessional = SessionalTable.objects.filter(uuid=pk).first()
    cos = CourseOutcome.objects.filter(subject=sessional.subject)
    data = {
        'Student': sessional.student_info
    }

    for co in cos:
        data[f'CO{co.number}'] = {'CT1':{},
                                  'CT2':{},
                                  'PUT':{},
                                  'A/T':{},}

    for key, value in sessional.ct1.items():
        for k, v in value.items():
            # add validation
            if v =='':
                data[key]['CT1'][k] = 0
            else:
                data[key]['CT1'][k] = v
    
    for key, value in sessional.ct2.items():
        for k, v in value.items():
            # add validation
            if v =='':
                data[key]['CT2'][k] = 0
            else:
                data[key]['CT2'][k] = v
        
    for key, value in sessional.put.items():
        for k, v in value.items():
            # add validation
            if v =='':
                data[key]['PUT'][k] = 0
            else:
                data[key]['PUT'][k] = v

    for key, value in sessional.assignment_tutorial.items():
        for k, v in value.items():
            # add validation
            if v =='':
                data[key]['A/T'][k] = 0
            else:
                data[key]['A/T'][k] = v
    
            
    print(data)
    df = pd.DataFrame(data)    

    

    

    # df = pd.DataFrame(data)

    current_datetime = datetime.now().strftime('%d_%H-%M-%S')

    pdf_file_name = f'table-{sessional.subject.code}-{current_datetime}.pdf'
    pdf = SimpleDocTemplate(pdf_file_name, pagesize=letter)

    table_data = [df.columns.to_list()] + df.values.tolist()

    table = Table(table_data)

    # style = TableStyle([
    #     ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header background color
    #     ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header text color
    #     ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align all cells
    #     ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Grid lines
    #     ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font bold
    #     ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Header bottom padding
    #     ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),  # Body font
    #     ('FONTSIZE', (0, 0), (-1, -1), 8),  # Font size
    #     ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),  # Inner grid lines
    #     ('BOX', (0, 0), (-1, -1), 0.25, colors.black),  # Outer border
    # ])
    # table.setStyle(style)

    # Add a centered heading above the table
    heading = "Sessional Table"
    heading_style = ParagraphStyle(
        'Heading1',
        parent=getSampleStyleSheet()['Heading1'],
        alignment=TA_CENTER,
    )
    heading_paragraph = Paragraph(heading, heading_style)
    elements = [heading_paragraph, Spacer(1, 12), table]

    # Build the PDF document
    pdf.build(elements)


    with open(pdf_file_name, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{pdf_file_name}"'
        return response
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{pdf_file_name}.csv"'

    # csv_writer = csv.writer(response)

    # csv_writer.writerow(list(cos.first().program_outcome_priority.keys())+list(cos.first().program_specific_outcome_priority[selected_department].keys())+list(cos.first().program_educational_objective_priority[selected_department].keys()))
    # for co in cos:
    #     csv_writer.writerow(list(co.program_outcome_priority.values())+list(co.program_specific_outcome_priority[selected_department].values())+list(co.program_educational_objective_priority[selected_department].values()))
    
    # df.to_csv(response, index=False)
    
    # return response   

