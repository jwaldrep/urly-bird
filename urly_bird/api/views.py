from bookmark.models import Bookmark, Click
from api.serializers import BookmarkSerializer, ClickSerializer
from rest_framework import viewsets


class BookmarkViewSet(viewsets.ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # FIXME: Breaks on anon user

class ClickViewSet(viewsets.ModelViewSet):
    queryset = Click.objects.all()
    serializer_class = ClickSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # FIXME: Breaks on anon user
