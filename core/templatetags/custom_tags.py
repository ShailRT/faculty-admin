from django import template 
from django.urls import resolve, reverse

register = template.Library()

@register.filter
def render_head(co_list):
    return [x for x in co_list.first().program_outcome_priority.keys()]

@register.simple_tag
def render_data(data, x, y):
    counter = 0
    for key in data.keys():
        if counter == x:
            return data[key][y]
        counter += 1

@register.filter
def divide(value, arg):
    try:
        return round(float(value) / float(arg), 2)
    except (ValueError, ZeroDivisionError):
        return None

@register.simple_tag(takes_context=True)
def breadcrumbs(context):
    request = context['request']
    path = request.path
    url_names = {
        '': ('Dashboard', reverse('dashboard')),
        'add-subject': ('Subjects', reverse('add-subject')),
        'sessional-table': ('Sessional Table', reverse('sessional-table')),
        'exit-survey' : ('Exit Survey', reverse('exit-survey')),
        'session' : ('Session', reverse('session-list')),
    }
    breadcrumbs = []
    try:
        resolver_match = resolve(path)
        breadcrumb_parts = path.strip('/').split('/')
        print(breadcrumb_parts)
        for i in range(len(breadcrumb_parts)):
            part = '/'.join(breadcrumb_parts[:i+1])
            if part in url_names:
                name = url_names[part][0]
                url = url_names[part][1]
                breadcrumbs.append((name, url))
    except:
        pass
    return breadcrumbs