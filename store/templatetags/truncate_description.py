from django import template
from django.template.defaultfilters import stringfilter
# import textwrap

register = template.Library()

@register.filter
@stringfilter
def truncate_middle(value):
    # divided_content = list(textwrap.wrap(value, 25))
    if "<br>" in value: # for HTML
        divided_content = value.split("<br>")
        if len(divided_content) <= 3:
            return " ".join(divided_content)
        return " ... ".join(divided_content[1:3] + divided_content[-3:-1]) # return first and last two elements of list.
    if "--" in value: # for RTF
        divided_content = value.split("--")
        return " ".join(divided_content[:len(divided_content) // 5]) + "..."
    return value # for plain TXT & other formats, don't shrink size