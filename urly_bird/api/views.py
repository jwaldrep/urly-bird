from django.contrib.auth.models import User
from bookmark.models import Bookmark, Click
from api.serializers import BookmarkSerializer, ClickSerializer, UserSerializer
from rest_framework import viewsets
from api.permissions import IsOwnerOrReadOnly, OwnsRelatedBookmark
from rest_framework import viewsets, permissions, generics, filters, mixins
from rest_framework.exceptions import PermissionDenied
import django_filters
from django.db.utils import IntegrityError


class BookmarkFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(name="user", lookup_type="exact")  # FIXME: Can't filter on user
    url = django_filters.CharFilter(name="url", lookup_type="icontains")
    title = django_filters.CharFilter(name="title", lookup_type="icontains")
    description = django_filters.CharFilter(name="description", lookup_type="icontains")

    class Meta:
        model = Bookmark
        fields = ['user', 'url', 'title', 'description']

class BookmarkViewSet(viewsets.ModelViewSet):
    """Use user, url, title, and/or description GET parameters to filter."""
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = BookmarkFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # FIXME: Breaks on anon user
            # user is used for permissions as well as serializing


# class UserViewSet(viewsets.ModelViewSet):
class UserViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ClickViewSet(viewsets.ModelViewSet):
    serializer_class = ClickSerializer
    queryset = Click.objects.all()
    #source = click_set.count() -- tons of queries
    # TODO: annotate inside view to reduce number of queries

    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        try:
            serializer.save(user_id=self.request.user.id) #, bookmark=???)
        except IntegrityError:
            serializer.save(user_id="anonymous")  # FIXME: Make None; update model to accept None for anonymous
                    #  FIXME: Breaks on anon user
                    #  TODO: How to access bookmark?
                    # FIXME: self.request.user.id works, but is this okay to use as PrimaryKeyRelatedField??

    # def get_queryset(self):
    #     self.queryset = Click.objects.filter(bookmark__user=self.request.user)
    #     return super().get_queryset()
