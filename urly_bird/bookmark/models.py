from django.db import models
from django.contrib.auth.models import User
from hashids import Hashids
from random import randint
from django.core.urlresolvers import reverse


class Bookmark(models.Model):
    user = models.ForeignKey(User)
    url = models.URLField()
    short = models.CharField(max_length=20, unique=True, blank=True, default='', primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True)

    def save(self, *args, **kwargs):
        if self.short == '':
            self.short = create_short(randint(0, 10**10))
        super(Bookmark, self).save(*args, **kwargs) # Call the "real" save() method.
        # do_something_else()

    def get_absolute_url(self):
        return reverse('bookmark_detail', kwargs={'pk': self.pk})

def update_short(bookmark):
    bookmark.short = create_short(randint(0,10**16))
    bookmark.save()

def create_short(num):
    hashids = Hashids()
    return hashids.encode(num)