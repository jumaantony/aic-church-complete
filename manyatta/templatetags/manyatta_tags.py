from django import template
from django.db.models import Count

from ..models import Sermon, NewsEvent

register = template.Library()


@register.inclusion_tag('latest_sermons.html')
def show_latest_sermons():
    latest_sermons = Sermon.objects.filter(status='publish').order_by('-publish')[:5]
    return {'latest_sermons': latest_sermons}


@register.inclusion_tag('latest_news_event.html')
def show_latest_news_event():
    latest_news_event = NewsEvent.objects.filter(status='publish').order_by('-publish')[:5]
    return {'latest_news_event': latest_news_event}


@register.inclusion_tag('home_latest_sermons.html')
def home_latest_sermons():
    latest_sermons = Sermon.objects.filter(status='publish').order_by('-publish')[:3]
    return {'latest_sermons': latest_sermons}


@register.inclusion_tag('home_latest_news_event.html')
def home_latest_news_event():
    latest_news_event = NewsEvent.objects.filter(status='publish').order_by('-publish')[:3]
    return {'latest_news_event': latest_news_event}

