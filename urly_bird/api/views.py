from bookmark.models import Bookmark, Click
from api.serializers import BookmarkSerializer, ClickSerializer
from rest_framework import viewsets


class BookmarkViewSet(viewsets.ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # FIXME: Breaks on anon user

class ClickViewSet(viewsets.ModelViewSet):
    serializer_class = ClickSerializer
    # queryset = Click.objects.all()

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id) #, bookmark=???)  # FIXME: Breaks on anon user # TODO: How to access bookmark?
                    # FIXME: self.request.user.id works, but is this okay to use as PrimaryKeyRelatedField??
    def get_queryset(self):
        self.queryset = Click.objects.filter(bookmark__user=self.request.user)
        return super().get_queryset()
