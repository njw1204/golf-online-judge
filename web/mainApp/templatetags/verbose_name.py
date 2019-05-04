from django import template
register = template.Library()

@register.simple_tag
def get_verbose_field_name(instance, field_name):
    return instance._meta.get_field(field_name).verbose_name

@register.filter
def human_readable(value, arg):
    if hasattr(value, 'get_' + str(arg) + '_display'):
        return getattr(value, 'get_%s_display' % arg)()
    elif hasattr(value, str(arg)):
        if callable(getattr(value, str(arg))):
            return getattr(value, arg)()
        else:
            return getattr(value, arg)
    else:
       try:
           return value[arg]
       except KeyError:
           return ""
