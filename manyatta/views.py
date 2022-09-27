import hashlib
import logging
from django.conf import settings
from django.contrib import messages
from django.contrib.postgres.search import SearchVector
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, ListView

from .models import Sermon, NewsEvent
from .forms import EmailForm, ContactForm

from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError

logger = logging.getLogger(__name__)

mailchimp = Client()
mailchimp.set_config({
    'api_key': settings.MAILCHIMP_API_KEY,
    'server': settings.MAILCHIMP_REGION,
})


# Create your views here.
# view used to check if there is successful connection between mailchimp and the app
def mailchimp_ping_view(request):
    response = mailchimp.ping.get()
    return JsonResponse(response)


def subscribe_view(request):
    if request.method == 'POST':
        email = request.POST['subscriber_email']
        try:
            form_email = email

            # member info contains the user information that will be stored in mailchimp
            member_info = {
                'email_address': form_email,
                'status': 'subscribed',
            }
            response = mailchimp.lists.add_list_member(
                settings.MAILCHIMP_MARKETING_AUDIENCE_ID,
                member_info)
            logger.info(f'API call successful: {response}')
            return redirect('manyatta:subscribe_success')

        except ApiClientError as error:
            logger.error(f'An exception occurred: {error.text}')
            return redirect('manyatta:subscribe_fail')


def index(request):
    return render(request, 'index.html')


def subscribe_success_view(request):
    return render(request, 'message.html', {
        'title': 'Successfully subscribed',
        'message': 'Yay, you have been successfully subscribed to our mailing list.',
        'unsubscribe-link': ''
    })


def subscribe_fail_view(request):
    return render(request, 'message.html', {
        'title': 'Failed to subscribe',
        'message': 'Oops, something went wrong.',
    })


def unsubscribe_view(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            try:
                form_email = form.cleaned_data['email']
                # hashing the user's email using md5 to generate a subscriber hash will allow to manipulate the
                # user's data
                form_email_hash = hashlib.md5(form_email.encode('utf-8').lower()).hexdigest()

                # member_update used to change the user data
                member_update = {
                    'status': 'unsubscribed',
                }
                response = mailchimp.lists.update_list_member(
                    settings.MAILCHIMP_MARKETING_AUDIENCE_ID,
                    form_email_hash,
                    member_update,
                )
                logger.info(f'API call successful: {response}')
                return redirect('manyatta:unsubscribe_success')

            except ApiClientError as error:
                logger.error(f'An exception occurred: {error.text}')
                return redirect('manyatta:unsubscribe_fail')

    return render(request, 'unsubscribe.html', {
        'form': EmailForm(),
    })


def unsubscribe_success_view(request):
    return render(request, 'message.html', {
        'title': 'Successfully unsubscribed',
        'message': 'You have been successfully unsubscribed from our mailing list.',
    })


def unsubscribe_fail_view(request):
    return render(request, 'message.html', {
        'title': 'Failed to unsubscribe',
        'message': 'Oops, something went wrong.',
    })


def about(request):
    return render(request, 'about.html')


def sermon_list(request):
    sermons = Sermon.objects.filter(status='publish').order_by('-publish')

    p = Paginator(sermons, 6)  # paginator object
    # getting the desired page number from url
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return the last page
        page_obj = p.page(p.num_pages)

    return render(request, 'sermonlist.html', {'sermons': page_obj})


def sermon_detail(request, year, month, day, sermon):
    sermon = get_object_or_404(Sermon, slug=sermon,
                               status='publish',
                               publish__year=year,
                               publish__month=month,
                               publish__day=day)

    return render(request, 'sermon_detail.html', {'sermon': sermon})


class NewsEventList(ListView):
    queryset = NewsEvent.objects.filter(status='publish').order_by('-publish')
    template_name = 'newsneventslist.html'
    paginate_by = 6


# def news_events_list(request):
#     news_events = NewsEvent.objects.filter(status='publish').order_by('-publish')
#     paginator = Paginator(news_events, 6)  # Show 25 contacts per page.
#
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#
#     return render(request, 'newsneventslist.html', {'news_events': news_events,
#                                                     'page_obj': page_obj})


class NewsEventDetail(DetailView):
    model = NewsEvent
    template_name = 'newsnevents_detail.html'


# def news_events_detail(request, year, month, day, news_event):
#     news_event = get_object_or_404(NewsEvent, slug=news_event,
#                                    status='publish',
#                                    publish__year=year,
#                                    publish__month=month,
#                                    publish__day=day)
#     return render(request, 'newsnevents_detail.html', {'news_event': news_event})


def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        form_data = {
            'name': name,
            'email': email,
            'message': message,
        }
        message = '''
            From:\n\t\t{}\n
            Message:\n\t\t{}\n
            Email:\n\t\t{}\n
            '''.format(form_data['name'], form_data['message'], form_data['email'],)
        send_mail('You got a mail!', message, '', ['jumaanton98@gmail.com'])
        messages.success(request, 'Your email has been sent successfully. We will reach out to you as soon as possible')
        return render(request, 'contact.html')

    else:
        return render(request, 'contact.html', {})


def search(request):
    if request.method == 'GET':
        query = request.GET['search_query']
        search_results = Sermon.objects.filter(status='publish').annotate(
            search=SearchVector('title', 'content'), ).filter(search=query)

    return render(request, 'search.html', {'query': query,
                                           'search_results': search_results, })


def men(request):
    return render(request, 'menministry.html')


def women(request):
    return render(request, 'womenministry.html')


def sunday_school(request):
    return render(request, 'sundayschoolministry.html')


def youth(request):
    return render(request, 'youthministry.html')


def praise_worship(request):
    return render(request, 'praisenworship.html')
