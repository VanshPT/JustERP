from django import template
from home.models import Module
register=template.Library()

@register.filter(name='not_in_deny_list')
def not_in_deny_list(value):
    """
    Check if the value is not in the deny list.
    Usage: {{ value|not_in_deny_list }}
    """
    deny_list = ["support", "users", "profile"]
    return value not in deny_list