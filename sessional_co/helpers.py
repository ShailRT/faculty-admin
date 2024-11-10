from io import BytesIO
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa 
import uuid 
from django.conf import settings 
import os
from core.models import CourseOutcome

def save_pdf(params:dict):
    template = get_template('pdf.html')
    html = template.render(params)
    response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), response)
    file_name = uuid.uuid4()
    base_url = "file://" + str(settings.BASE_DIR) + "/pdf/"
    try:
        with open(str(settings.BASE_DIR) + f'/pdf/{file_name}.pdf', 'wb+') as output:
            pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), output, link_callback=lambda uri, _: os.path.join(base_url, uri))

    except Exception as e:
        print(e) 
    
    if pdf.err:
        return '', False
    
    return file_name, True


def calculate_sessional_attainment(table):
    print("table", table)
    cos = CourseOutcome.objects.filter(subject=table.subject)
    co_attainment = {}
    for co in cos:
        co_attainment[f'CO{co.number}'] = {
            'count': 0,
            'percentage': 0.0,
            'level': 0,
        }

    for co in cos:
        for rollno in table.ct1.keys():
            temp = {
                'ct1': 0,
                'ct2': 0,
                'put': 0,
                'ant': 0
            }
            for qno, qval in table.ct1[rollno][f'CO{co.number}'].items():
                for marks in qval.values():
                    temp['ct1'] += int(marks)
            for qno, qval in table.ct2[rollno][f'CO{co.number}'].items():
                for marks in qval.values():
                    temp['ct2'] += int(marks)
            for qno, qval in table.put[rollno][f'CO{co.number}'].items():
                for marks in qval.values():
                    temp['put'] += int(marks)
            
            temp['ant'] += int(table.assignment_tutorial[rollno][f'CO{co.number}'])
            if (temp['ct1'] + temp['ct2'] + temp['put'] + temp['ant']) != 0 and (table.max_marks['ct1'][f'CO{co.number}'] + table.max_marks['ct2'][f'CO{co.number}'] + table.max_marks['put'][f'CO{co.number}'] + table.max_marks['ant'][f'CO{co.number}']) != 0:
                if ((temp['ct1'] + temp['ct2'] + temp['put'] + temp['ant']) / (table.max_marks['ct1'][f'CO{co.number}'] + table.max_marks['ct2'][f'CO{co.number}'] + table.max_marks['put'][f'CO{co.number}'] + table.max_marks['ant'][f'CO{co.number}'])) * 100 >= 70.0:
                    co_attainment[f'CO{co.number}']['count'] += 1
    
    for co in co_attainment.keys():

        co_attainment[co]['percentage'] = (co_attainment[co]['count'] / len(table.session.students.all()) ) * 100
        if co_attainment[co]['percentage'] < 50.0 :
            co_attainment[co]['level'] = 1
        elif co_attainment[co]['percentage'] < 60.0:
            co_attainment[co]['level'] = 2
        else:
            co_attainment[co]['level'] = 3
            
    return co_attainment
                