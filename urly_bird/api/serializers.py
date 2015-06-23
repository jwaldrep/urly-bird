from bookmark.models import Bookmark
from rest_framework import serializers

class BookmarkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bookmark
        fields = ('id', 'url', 'user', 'short', 'timestamp', 'title', 'description') # FIXME: Okay to name url?, readonly?

