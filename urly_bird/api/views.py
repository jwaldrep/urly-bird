from bookmark.models import Bookmark
from api.serializers import BookmarkSerializer
from rest_framework import viewsets


class BookmarkViewSet(viewsets.ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # FIXME: Breaks on anon user