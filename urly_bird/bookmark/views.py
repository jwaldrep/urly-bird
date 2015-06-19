from django.shortcuts import render

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from bookmark.models import Bookmark

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

class BookmarkUpdate(UpdateView):
    model = Bookmark
    fields = ['url', 'title', 'description']

class BookmarkDelete(DeleteView):
    model = Bookmark
    success_url = reverse_lazy('bookmark_list')
