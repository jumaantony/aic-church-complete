from django.urls import path
from . import views

app_name = 'manyatta'

urlpatterns = [
    # ping mailchimp
    path('ping/', views.mailchimp_ping_view, name='ping'),

    path('', views.index, name='index'),

    path('search/', views.search, name='search'),

    path('subscribe', views.subscribe_view, name='subscribe'),

    path('success/', views.subscribe_success_view, name='subscribe_success'),

    path('fail/', views.subscribe_fail_view, name='subscribe_fail'),

    path('unsubscribe/', views.unsubscribe_view, name='unsubscribe'),

    path('unsubscribe/success/', views.unsubscribe_success_view, name='unsubscribe_success'),

    path('unsubscribe/fail/', views.unsubscribe_fail_view, name='unsubscribe_fail'),

    path('about/', views.about, name='about'),

    path('sermon_list/', views.sermon_list, name='sermon_list'),

    path('<int:year>/<int:month>/<int:day>/<slug:sermon>/', views.sermon_detail, name='sermon_detail'),

    path('contact_us/', views.contact_us, name='contact_us'),

    path('mens-ministry/', views.men, name='mens-ministry'),

    path('womens-ministry/', views.women, name='womens-ministry'),

    path('sundayschool-ministry/', views.sunday_school, name='sundayschool-ministry'),

    path('youth-ministry/', views.youth, name='youth-ministry'),

    path('praisenworship-ministry/', views.praise_worship, name='praisenworship-ministry'),

    path('news_events_list/', views.NewsEventList.as_view(), name='news_events_list'),

    path('<slug:slug>/', views.NewsEventDetail.as_view(), name='news_events_detail'),

    

    # path('news_events_list/', views.news_events_list, name='news_events_list'),
    #
    # path('<int:year>/<int:month>/<int:day>/<slug:news_event>/', views.news_events_detail, name='news_events_detail'),

]
