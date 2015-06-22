from django.contrib import admin
from .models import Bookmark, Click


class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'url', 'short', 'timestamp', 'title',
                    'description']


admin.site.register(Bookmark, BookmarkAdmin)


class ClickAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'user_id', 'bookmark']


admin.site.register(Click, ClickAdmin)
