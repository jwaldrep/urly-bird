from django.contrib.auth.models import User
from bookmark.models import Bookmark, Click
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email')


class BookmarkSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    api_url = serializers.HyperlinkedIdentityField(view_name='bookmark-detail')  # FIXME: Huh?
    pk = serializers.PrimaryKeyRelatedField(read_only=True)
    num_clicks = serializers.IntegerField(source='click_set.count', read_only=True)

    class Meta:
        model = Bookmark
        fields = ('pk', 'url', 'user', 'api_url', 'timestamp', 'title', 'description', 'num_clicks') # FIXME: Okay to name url?, readonly?
            # FIXME: why does id break it? (django.core.exceptions.ImproperlyConfigured: Field name `id` is not valid for model `Bookmark`.)
            # FIXME: why does short show up twice? (pk == short, so remove short)

class ClickSerializer(serializers.HyperlinkedModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)
    # bookmark = serializers.PrimaryKeyRelatedField() # Can't be read_only initially
    # url = serializers.HyperlinkedIdentityField(view_name='click-detail') # FIXME: Is this needed? No, doesn't solve the problem

    class Meta:
        model = Click
        fields = ('id', 'url', 'user_id', 'bookmark', 'timestamp')