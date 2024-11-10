from .models import CourseOutcome
from sessional_co.models import SessionalTable
from sessional_co.helpers import calculate_sessional_attainment

def get_average_attainment(subject, session):
    
    # Get Internal Attainment 
    print("session", session)
    session_co = SessionalTable.objects.filter(session=session).first()
    internal_attainment = calculate_sessional_attainment(session_co)

    cos = CourseOutcome.objects.filter(subject=subject)
    # for co in cos:
    #     internal_attainment[f'CO{co.number}'] = {
    #     'count': 0,
    #     'percentage': 0.0,
    #     'level': 0
    # }
    # sessional_marks = session_co.ct1
    # for key, value in session_co.ct2.items():
    #     for ke, val in value.items():
    #         sessional_marks[key][ke] += val
    # for key, value in session_co.put.items():
    #     for ke, val in value.items():
    #         sessional_marks[key][ke] += val
    # for key, value in session_co.assignment_tutorial.items():
    #     for ke, val in value.items():
    #         sessional_marks[key][ke] += val

    # max_marks = {}
    # for key, value in session_co.max_marks.items():
    #     max_marks[key] = 0
    #     for val in value.values():
    #         max_marks[key] += val
    
    # for key, value in sessional_marks.items():
    #     for val in value.values():
    #         if val!='' and (float(val)/max_marks[key])*100 >= 70.0:
    #             internal_attainment[key]['count'] += 1
    
    total_students = len(session.students.all())
    
    # for key in internal_attainment.keys():
        # internal_attainment[key]['percentage'] = (internal_attainment[key]['count'] / total_students) * 100
        # if  internal_attainment[key]['percentage'] < 50.0 :
        #     internal_attainment[key]['level'] = 1
        # elif internal_attainment[key]['percentage'] <= 60.0 :
        #     internal_attainment[key]['level'] = 2
        # else:
        #     internal_attainment[key]['level'] = 3
            
    # Get External Attainment 
    external_attainment ={
        'count': 0,
        'percentage': 0.0,
        'level': 0
    }
    for student in session.students.all():
        if float(student.final_marks[subject.code]['scored'])/float(student.final_marks[subject.code]['max-marks'])*100 >= 50.0:
            external_attainment['count'] += 1
    external_attainment['percentage'] = (external_attainment['count']/total_students)*100
    if external_attainment['percentage'] < 50.0:
        external_attainment['level'] = 1
    elif external_attainment['percentage'] < 60:
        external_attainment['level'] = 2
    else:
        external_attainment['level'] = 3
    
    # Get Indirect Attainment 
    indirect_attainment = {}
    for co in cos:
        indirect_attainment[f'CO{co.number}'] = {
        'count': 0,
        'percentage': 0.0,
        'level': 0
    }
    for student in session.students.all():
        for key, value in student.co_response[subject.code].items():
            if int(value) >=3:
                indirect_attainment[key]['count'] += 1
    
    for value in indirect_attainment.values():
        value['percentage'] = (value['count']/total_students)*100
        if value['percentage'] < 50:
            value['level'] = 1
        elif value['percentage'] < 60:
            value['level'] = 2
        else:
            value['level'] = 3
    
    final_attainment = {
        }
    total_final_attain = 0
    for co in cos:
        temp = final_attainment[f'CO{co.number}'] = round(0.8*(0.2*internal_attainment[f'CO{co.number}']['level']+0.8*external_attainment['level'])+0.2*indirect_attainment[f'CO{co.number}']['level'], 2)
        total_final_attain += temp
    
    # final_attainment['internal'] = internal_attainment
    # final_attainment['external'] = external_attainment
    # final_attainment['indirect'] = indirect_attainment
    final_attainment['avg_attainment'] = round(total_final_attain/len(cos), 2)
    
    return final_attainment
    