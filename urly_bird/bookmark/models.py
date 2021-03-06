from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import make_aware, now
from hashids import Hashids
from random import randint, choice
from django.core.urlresolvers import reverse
from faker import Faker

from django.db.utils import IntegrityError


class Bookmark(models.Model):
    user = models.ForeignKey(User)
    url = models.URLField()
    short = models.CharField(max_length=20, unique=True, blank=True,
                             default='', primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True)

    def __str__(self):
        return '{} @ {} : {} = {}'.format(self.user, self.timestamp,
                                          self.short, self.timestamp, self.url)

    def save(self, *args, **kwargs):
        #  def try_short(self):   # FIXME: Try again if there's a hash collision
        #      if self.short == '':
        #          try:
        #              self.short = create_short(randint(0,2))#randint(0, 10**10))
        #          except IntegrityError:
        #              return try_short(self)
        #  try_short(self)
        #
        self.short = create_short(randint(0, 10 ** 16))

        super().save(*args, **kwargs)  # Call the "real" save() method.
        # do_something_else()

    def get_absolute_url(self):
        return reverse('bookmark_detail', kwargs={'pk': self.pk})


def create_short(num):
    hashids = Hashids()
    return hashids.encode(num)


def create_fake_users(num=10):
    fake = Faker()
    for _ in range(num):
        user = User.objects.create_user(username=fake.name(),
                                        email=fake.email(),
                                        password='password')
        # user.save()


def create_fake_bookmarks(user, num=10):
    # TODO: Change model to allow fake Bookmark timestamp
    fake = Faker()
    for _ in range(num):
        url = fake.uri()
        timestamp = make_aware(fake.date_time_this_month())
        title = fake.bs()
        description = fake.catch_phrase()
        bookmark = Bookmark(user=user, url=url, timestamp=timestamp,
                            title=title, description=description)
        bookmark.save()


class Click(models.Model):
    bookmark = models.ForeignKey(Bookmark)
    timestamp = models.DateTimeField(default=now)
    user_id = models.CharField(max_length=16) # FIXME: FK to user, add null=True

    def __str__(self):
        return '@' + str(self.timestamp) + '->' + str(self.bookmark)


def create_fake_clicks(bookmarks, num=10, random=True,
                       timefn=Faker().date_time_this_month):
    """
        Create `num` fake clicks for each bookmark with timestep
        given a set of bookmark objects (bookmarks).
        If random is True, create between 1 and `num` clicks for each combo.

        Example Usage:
        bs = Bookmark.objects.all().filter(user_id=1)
        create_fake_clicks(bs, num=3)
    """
    for bookmark in bookmarks:
        users = User.objects.all()
        for _ in range(randint(1, num)):
            click = Click(bookmark=bookmark, timestamp=make_aware(timefn()),
                          user_id=choice(
                              users).id)  # FIXME: pick random user, test
            click.save()
