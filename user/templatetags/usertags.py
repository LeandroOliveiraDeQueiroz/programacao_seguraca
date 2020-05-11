from django import template
from programacao_e_seguranca.settings import AXES_FAILURE_LIMIT, AXES_COOLOFF_TIME
from axes.models import AccessAttempt
from datetime import *
from django.utils import timezone



register = template.Library()

@register.filter(name="pretty_time_delta")
def pretty_time_delta(seconds):
    seconds = int(seconds)
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    if days > 0:
        return '%dd%dh%dm%ds' % (days, hours, minutes, seconds)
    elif hours > 0:
        return '%dh%dm%ds' % (hours, minutes, seconds)
    elif minutes > 0:
        return '%dm%ds' % (minutes, seconds)
    else:
        return '%ds' % (seconds,)


@register.filter(name="axes_message")
def axes_message(username=None):
    
    time = timedelta(seconds=0)
    access = AccessAttempt.objects.filter(username=username).first()

    print(access.attempt_time)
    
    if access:
        time = AXES_COOLOFF_TIME - (timezone.now() - access.attempt_time)
    
    pretty_time = pretty_time_delta(time.seconds)
    msg = 'Sua conta foi <strong>bloqueada</strong> após a {}º tentativa de acesso. Tente novamente em <strong>{}</strong>.'.format(AXES_FAILURE_LIMIT, pretty_time)
    return msg