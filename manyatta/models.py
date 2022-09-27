from django.db import models
from django.utils import timezone
from django.urls import reverse

from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.
class Sermon(models.Model):
    STATUS_CHOICES = (
        ('draft', 'draft'),
        ('publish', 'publish')
    )
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique_for_date='publish')
    feature_img = models.ImageField(blank=True, null=True, upload_to='feature_img')
    preacher = models.CharField(max_length=50)
    readings = models.CharField(max_length=200)
    content = RichTextUploadingField()
    created = models.DateTimeField(auto_now_add=True)
    publish = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('manyatta:sermon_detail', args=[self.publish.year,
                                                       self.publish.month,
                                                       self.publish.day,
                                                       self.slug])


class NewsEvent(models.Model):
    STATUS_CHOICES = (
        ('draft', 'draft'),
        ('publish', 'publish')
    )
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique_for_date='publish')
    feature_img = models.ImageField(blank=True, null=True, upload_to='feature_img')
    content = RichTextUploadingField()
    organizer = models.CharField(max_length=200, blank=True, null=True)
    commence_date = models.DateTimeField(blank=True, null=True)
    ending_date = models.DateTimeField(blank=True, null=True)
    entry_fee = models.DecimalField(decimal_places=0, max_digits=5, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    publish = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse('manyatta:news_events_detail', args=[self.publish.year,
    #                                                         self.publish.month,
    #                                                         self.publish.day,
    #                                                         self.slug])
