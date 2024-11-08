
from django import template

register = template.Library()

@register.filter
def mask_email(email):
    if "@" not in email:
        return email 

    local_part, domain = email.split("@")
    masked_email = local_part[:3] + "*" * (len(local_part) - 3) + "@" + domain
    return masked_email
