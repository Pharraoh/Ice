from django import template

register = template.Library()

@register.filter
def get_content(messages):
    if messages:
        last_message = messages.last()
        return getattr(last_message, 'content', '')
    return ''
