from django.shortcuts import render
from django.views.generic import ListView

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


class BookmarkListView(ListView):
    template_name = "bookmarks/bookmark_list.html"
    model = Bookmark
    context_object_name = 'bookmarks'
    queryset = Bookmark.objects.order_by('-timestamp', ) #.annotate(Count('favorite')).select_related()
    paginate_by = 20
    header = "All bookmarks"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = self.header
        # if self.request.user.is_authenticated():
        #     favorites = self.request.user.favorited_bookmarks.all()
        # else:
        #     favorites = []
        # context["favorites"] = favorites
        return context

class IndexView(BookmarkListView):
    template_name = "index.html"