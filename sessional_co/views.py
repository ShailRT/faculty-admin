from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from core.models import Subject, CourseOutcome, AccessRequest
from .models import SessionalTable
from .forms import SessionalTableCreateForm
from exit_survey.models import SessionStudent
import pandas as pd
from xhtml2pdf import pisa
from django.template.loader import get_template
from .helpers import calculate_sessional_attainment


def sessional_list(request):
    if request.method == "POST":
        form = SessionalTableCreateForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.faculty = request.user
            cos = CourseOutcome.objects.filter(subject=form.subject)
            ct_json = {}
            put_json = {}
            ant_json = {}
            max_marks = {
                'ct1': {},
                'ct2': {},
                'put': {},
                'ant': {}
            }
            for student in form.session.students.all():
                ct_json[str(student.university_roll_no)] = {}
                put_json[str(student.university_roll_no)] = {}
                ant_json[str(student.university_roll_no)] = {}
                for co in cos:
                    ct_json[str(student.university_roll_no)][f"CO{co.number}"] = {
                        'Question-1': {
                            'a': 0,
                            'b': 0,
                            'c': 0,
                            'd': 0,
                            'e': 0,
                        }, 'Question-2': {
                            'a': 0,
                            'b': 0,
                            'c': 0,
                            'd': 0,
                            'e': 0,
                        }, 'Question-3': {
                            'a': 0,
                            'b': 0,
                            'c': 0,
                        }
                    }
                    
                    put_json[str(student.university_roll_no)][f"CO{co.number}"] = {
                        'Question-1': {
                            'a': 0,
                            'b': 0,
                            'c': 0,
                            'd': 0,
                            'e': 0,
                            'f': 0,
                            'g': 0,
                        }, 'Question-2': {
                            'a': 0,
                            'b': 0,
                            'c': 0,
                            'd': 0,
                            'e': 0,
                            'f': 0,
                            'g': 0,
                        }, 'Question-3': {
                            'a': 0,
                            'b': 0,
                        }, 'Question-4': {
                            'a': 0,
                            'b': 0,
                        }, 'Question-5': {
                            'a': 0,
                            'b': 0,
                        }, 'Question-6': {
                            'a': 0,
                            'b': 0,
                        }, 'Question-7': {
                            'a': 0,
                            'b': 0,
                        }
                    }
                    ant_json[str(student.university_roll_no)][f"CO{co.number}"] = 0
                    max_marks['ct1'][f'CO{co.number}'] = 0
                    max_marks['ct2'][f'CO{co.number}'] = 0
                    max_marks['put'][f'CO{co.number}'] = 0
                    max_marks['ant'][f'CO{co.number}'] = 0
            
            form.ct1, form.ct2, form.put, form.assignment_tutorial = ct_json, ct_json, put_json, ant_json
            form.max_marks = max_marks
            form.save()
        else:
            print(form.errors)
        return redirect('sessional-table')
        
    form = SessionalTableCreateForm()
    sessions = SessionStudent.objects.all()
    subjects = Subject.objects.all()
    sessionals = SessionalTable.objects.filter(faculty=request.user)
    context = {
        'subjects': subjects,
        'sessionals': sessionals,
        'sessions': sessions,
        'form': form
    }
    return render(request, 'sessional-list.html', context)

def sessional_table_edit(request, pk, field):
    table = SessionalTable.objects.filter(uuid=pk).first()
    subject = table.subject
    table_header = ['R.N']
    if field == 'ct1':
        table_dict = table.ct1
        table_header.append([{'Question-1': ['a', 'b', 'c', 'd', 'e']}, {'Question-2': ['a', 'b', 'c', 'd', 'e']}, {'Question-3': ['a', 'b', 'c']}])
    elif field == 'ct2':
        table_dict = table.ct2
        table_header.append([{'Question-1': ['a', 'b', 'c', 'd', 'e']}, {'Question-2': ['a', 'b', 'c', 'd', 'e']}, {'Question-3': ['a', 'b', 'c']}])
    elif field == 'put':
        table_dict = table.put
        table_header.append([{'Question-1': ['a', 'b', 'c', 'd', 'e', 'f', 'g']}, {'Question-2': ['a', 'b', 'c', 'd', 'e', 'f', 'g']}, {'Question-3': ['a', 'b']}, {'Question-4': ['a', 'b']}, {'Question-5': ['a', 'b']}, {'Question-6': ['a', 'b']}, {'Question-7': ['a', 'b']}])
    elif field == 'ant':
        table_dict = table.assignment_tutorial

    table_body = {}
    for key, value in table_dict.items():
        table_body[key] = {}
        for ke, val in value.items():
            table_body[key][ke] = {}
            for k, v in val.items():
                table_body[key][ke][k] = v.values()
    
    print("table HEader", table_header)
    print("-------")
    print("table body", table_body)
    
    context = {
        'table_header': table_header,
        'table_body': table_body,
        'field': field,
        'subject': subject,
        'table_uuid': table.uuid,
        'table_max_marks': table.max_marks[field]
    }

    if request.method == "POST":
        table = SessionalTable.objects.filter(uuid=pk).first()
        if field == 'ct1':
            table_dict = table.ct1
        elif field == 'ct2':
            table_dict = table.ct2
        elif field == 'put':
            table_dict = table.put
        elif field == 'ant':
            table_dict = table.assignment_tutorial
        
        for rollno, rollvalue in table_dict.items():
            for cono, coval in rollvalue.items():
                for qno, qval in coval.items():
                    temp = 0
                    for marks in qval.keys():
                        table_dict[rollno][cono][qno][marks] = int(request.POST[f'{rollno}_{cono}_{qno}_{temp}'])
                        temp+=1

        for co, marks in table.max_marks[field].items():
            table.max_marks[field][co] = int(request.POST[f'max_{co}'])
        try:
            table.save()
            messages.info(request, 'Table Updated!')
        except Exception as e: 
            print(e)
        return redirect('sessional-table-edit', pk=pk, field=field)
    
    return render(request, 'sessional-table-edit.html', context)

def test_pdf(request, pk):
    table = SessionalTable.objects.filter(uuid=pk).first()
    cos_all = CourseOutcome.objects.filter(subject=table.subject)
    field = request.GET.get('field')
    cos = []
    data = {}
    table_header = ['R.N']
    if field == 'ct1':
        table_dict = table.ct1
        table_header.append([{'Question-1': ['a', 'b', 'c', 'd', 'e']}, {'Question-2': ['a', 'b', 'c', 'd', 'e']}, {'Question-3': ['a', 'b', 'c']}])
    elif field == 'ct2':
        table_dict = table.ct2
        table_header.append([{'Question-1': ['a', 'b', 'c', 'd', 'e']}, {'Question-2': ['a', 'b', 'c', 'd', 'e']}, {'Question-3': ['a', 'b', 'c']}])
    elif field == 'put':
        table_dict = table.put
        table_header.append([{'Question-1': ['a', 'b', 'c', 'd', 'e', 'f', 'g']}, {'Question-2': ['a', 'b', 'c', 'd', 'e', 'f', 'g']}, {'Question-3': ['a', 'b']}, {'Question-4': ['a', 'b']}, {'Question-5': ['a', 'b']}, {'Question-6': ['a', 'b']}, {'Question-7': ['a', 'b']}])
    elif field == 'ant':
        table_dict = table.assignment_tutorial
    
    table_body = {}
    for key, value in table_dict.items():
        table_body[key] = {}
        for ke, val in value.items():
            table_body[key][ke] = {}
            for k, v in val.items():
                table_body[key][ke][k] = v.values()
    

    data['header'], data['body'] = table_header, table_body

    result_calc = calculate_sessional_attainment(table)
    print(result_calc)
    

    # max_marks = {}
    # co_attainment = {}
    # value = list(data.values())[0]
    # for co in cos_all:
    #     for k, v in value.items():
    #         if k[-1] == co.number and co not in cos:
    #             cos.append(co)
    #             break
    # for co in cos:
    #     co_attainment[f'CO{co.number}'] =  {
    #         'count':0,
    #         'percentage': 0,
    #         'level': 0,
    #     }
    
    # for key, value in sessional.max_marks.items():
    #     max_marks[key] = sum(value.values())
    # for key, value in data.items():
    #     for ke, val in value.items():
    #         total = 0
    #         for k, v in val.items():
    #             if v!='':
    #                 total+=int(v)
    #             else:
    #                 total+=0
    #         if total == 0 or max_marks[ke] == 0:
    #             value[ke]['percentage'] = 0
    #         else:
    #             temp = round((total/max_marks[ke])*100, 2)
    #             value[ke]['percentage'] = temp
    #             if temp >= 70.0:
    #                 co_attainment[ke]['count'] += 1
    # total_student = len(sessional.session.students.all())
    # for co in co_attainment.keys():
    #     co_attainment[co]['percentage'] = (co_attainment[co]['count'] / total_student)*100
    #     if co_attainment[co]['percentage'] < 50.0 :
    #         co_attainment[co]['level'] = 1
    #     elif co_attainment[co]['percentage'] <= 60.0 :
    #         co_attainment[co]['level'] = 2
    #     else:
    #         co_attainment[co]['level'] = 3
    
    # split_value = 2 if len(cos)<5 else 3
    
    params = {
        'cos': cos,
        'data': data,
        'table_session': table.session, 
        'table_semester': table.semester,
        'table_odd_or_even': 'Odd' if int(table.semester[0])%2==1 else 'Even',
        'table_faculty_name': table.faculty.first_name+' '+table.faculty.last_name,
        'table_subject': table.subject,
        'table_department': table.faculty.department,
        # 'co_attainment': co_attainment,
        # 'split_value': split_value,

    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f"filename='{table.subject.title}-{table.semester}.pdf'"

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


