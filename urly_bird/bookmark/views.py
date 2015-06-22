from braces.views import PermissionRequiredMixin
from django.forms import model_to_dict
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from bookmark.models import Bookmark, Click
from django.shortcuts import render, redirect
from django.db.models import Count, Avg
from django.utils import timezone
from datetime import datetime, timedelta


class BookmarkCreate(CreateView):
    model = Bookmark
    fields = ['url', 'title', 'description']
    # user = models.ForeignKey(User)
    # url = models.URLField()
    # short = models.CharField(max_length=20, unique=True, null=True, blank=True, default='')
    # timestamp = models.DateTimeField(auto_now_add=True)
    # title = models.CharField(max_length=255)
    # description = models.CharField(max_length=255, null=True)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(BookmarkCreate, self).form_valid(form)


class BookmarkUpdate(UpdateView):  # PermissionRequiredMixin
    model = Bookmark
    fields = ['url', 'title', 'description']
    # permission_required = "bookmark.change_bookmark"

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(BookmarkUpdate, self).get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj


class BookmarkDelete(DeleteView):
    model = Bookmark
    success_url = reverse_lazy('bookmark_list')

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(BookmarkDelete, self).get_object()
        if not obj.owner == self.request.user:
            raise Http404
        return obj


class BookmarkListView(ListView):
    template_name = "bookmarks/bookmark_list.html"
    model = Bookmark
    context_object_name = 'bookmarks'
    queryset = Bookmark.objects.order_by(
        '-timestamp', )  # .annotate(Count('favorite')).select_related()
    paginate_by = 20
    header = "All Bookmarks"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = self.header
        # if self.request.user.is_authenticated():
        #     favorites = self.request.user.favorited_bookmarks.all()
        # else:
        #     favorites = []
        # context["favorites"] = favorites
        return context


class UserBookmarkListView(BookmarkListView):
    header = "Personal Bookmarks"

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Bookmark.objects.filter(user_id=user_id).order_by(
            '-timestamp', ).annotate(
            num_clicks=Count('click')).select_related()
        # + TODO: A user's bookmark page should be public.
        # + When viewing a user's bookmark page when not that user, the links
        # + to edit and delete bookmarks should not show up.
        # + TODO: On a logged in user's index page,
        # + they should see a list of the bookmarks they've saved
        # + in reverse chronological order, paginated.
        # + The bookmark links should use the internal short-code route, not the original URL.
        # + From this page, they should be able to edit and delete bookmarks.


class IndexView(BookmarkListView):
    template_name = "index.html"

    def get_queryset(self):
        me = self.request.user.id
        return Bookmark.objects.all().annotate(
            num_clicks=Count('click')).order_by('-timestamp',
                                                '-num_clicks')  # .select_related()

        # + TODO: There should also be a page to view all bookmarks for all users
        # + in reverse chronological order, paginated.


def ClickView(request, pk):  # FIXME: Fix case
    # do something, then
    # When a user -- anonymous or logged in -- uses a bookmark URL, record that user, bookmark, and timestamp.
    bookmark = Bookmark.objects.get(pk=pk)
    user_id = request.user.id
    if not user_id:
        user_id = 'anonymous'
    click = Click(bookmark=bookmark, timestamp=timezone.now(),
                  user_id=user_id)
    click.save()
    return redirect(bookmark.url)


def MyBookmarksView(request):  # FIXME: Fix case
    user = request.user
    thirty_days_ago = timezone.now() - timedelta(days=30)
    mine = Bookmark.objects.filter(user=request.user).annotate(
        count_total=Count('click'))
    recent = Bookmark.objects.filter(
        click__timestamp__gte=thirty_days_ago).annotate(count_recent=Count(
        'click'))  # FIXME: Subquery 'mine' or Filter by user?

    return render(request, "dashboard.html", {'mine': mine,
                                              'recent': recent})


    # clicks = Click.objects.filter(timestamp__lte=datetime.today(),
    #                            timestamp__gt=datetime.today() - timedelta(
    #                                days=30)) #.values('createdate').annotate(count=Count('id'))


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib

matplotlib.style.use('fivethirtyeight')


def clicks_chart(request, pk):
    # TODO: Add a stats page for each link where you can see the traffic for that link for the last 30 days in a line chart.
    # FIXME: Add error checking if 0 clicks
    thirty_days_ago = timezone.now() - timedelta(days=30)
    clicks = Click.objects.filter(bookmark_id=pk).filter(
        timestamp__gte=thirty_days_ago)  # .annotate(count_recent=Count('click'))
    df = pd.DataFrame(model_to_dict(click) for click in clicks)
    df['count'] = 1
    df.index = df['timestamp']
    counts = df['count']
    counts = counts.sort_index()
    series = pd.expanding_count(counts).resample('D', how=np.max,
                                                 fill_method='pad')
    response = HttpResponse(content_type='image/png')

    fig = plt.figure()
    # ax = fig.add_subplot(111)
    # ax.plot(series)
    series.plot()
    plt.title("Total clicks over past 30 days")
    plt.xlabel("")
    plt.xlim(thirty_days_ago, timezone.now())
    canvas = FigureCanvas(fig)
    # ax = fig.add_subplot(1, 1, 1, axisbg='red')
    # ax.plot(series)
    canvas.print_png(response)
    return response


class ClickListView(ListView):
    template_name = "bookmarks/click_list.html"
    model = Click
    context_object_name = 'click'
    queryset = Click.objects.order_by(
        '-timestamp', )  # .select_related()  # FIXME: Fix missing queryset
    paginate_by = 20
    header = "All Clicks"

    # def get_queryset(self):
    #     me = self.request.user.id
    #     return Click.objects.order_by('-timestamp', )  # .select_related()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = self.header

        # TODO: Verify SQL queries are efficient
        # +TODO: Add an overall stats page for each user where you can see a table of their links by popularity and their number of clicks over the last 30 days. This page should only be visible to that user.
        # TODO: (opt) Add multiple views on index page
        # TODO: (opt) Add sorting/filtering mixins
        # TODO: (opt) Add plots
        # TODO: Add dropdown for weekly/montly/yearly/30 day totals
        # TODO: Add search for bookmarks
        # TODO: Differentiate dashboard vs user page
        # TODO: Add user profile
