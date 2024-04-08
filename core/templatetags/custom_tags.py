from django import template 

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
     

