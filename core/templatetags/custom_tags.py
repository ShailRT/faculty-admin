from django import template 

register = template.Library()

@register.filter
def render_head(co_list):
    return [x for x in co_list.first().program_outcome_priority.keys()]
