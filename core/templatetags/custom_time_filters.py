from django import template
from django.utils import timezone
from datetime import datetime, timedelta 

register = template.Library()

@register.filter
def custom_timesince(value):
    if not isinstance(value, (datetime, datetime.date)):
        return value

    now = timezone.now()
    delta = now - value

    
    seconds = delta.total_seconds()
    if seconds < 60:
        return f"{int(seconds)} seconds ago"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{int(minutes)} minutes ago"
    elif seconds < 86400:  
        hours = seconds // 3600
        return f"{int(hours)} hours ago"
    elif seconds < 604800:  
        days = seconds // 86400
        return f"{int(days)} days ago"
    elif seconds < 2419200:  
        weeks = seconds // 604800
        return f"{int(weeks)} weeks ago"
    elif seconds < 29030400: 
        months = seconds // 2419200
        return f"{int(months)} months ago"
    else:  
        years = seconds // 29030400
        return f"{int(years)} years ago"