from django.contrib import admin

from .models import Sermon, NewsEvent


# Register your models here.
@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'feature_img', 'preacher',
                    'readings', 'publish', 'status')
    list_filter = ('status', 'created', 'publish')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


@admin.register(NewsEvent)
class SermonAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'feature_img', 'organizer', 'commence_date',
                    'ending_date', 'entry_fee', 'publish', 'status')
    list_filter = ('status', 'created', 'publish')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')

