from bookmark.models import Bookmark, Click
from api.serializers import BookmarkSerializer, ClickSerializer
from rest_framework import viewsets
from api.permissions import IsOwnerOrReadOnly, OwnsRelatedBookmark
from rest_framework import viewsets, permissions, generics
from rest_framework.exceptions import PermissionDenied


class BookmarkViewSet(viewsets.ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # FIXME: Breaks on anon user
            # user is used for permissions as well as serializing
class ClickViewSet(viewsets.ModelViewSet):
    serializer_class = ClickSerializer
    # queryset = Click.objects.all()
    #source = click_set.count() -- tons of queries
    # TODO: annotate inside view to reduce number of queries

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id) #, bookmark=???)  # FIXME: Breaks on anon user # TODO: How to access bookmark?
                    # FIXME: self.request.user.id works, but is this okay to use as PrimaryKeyRelatedField??

    def get_queryset(self):
        self.queryset = Click.objects.filter(bookmark__user=self.request.user)
        return super().get_queryset()
