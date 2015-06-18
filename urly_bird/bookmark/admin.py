from django.contrib import admin
from .models import Bookmark

class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'url', 'short', 'timestamp', 'title', 'description']

# Register your models here.
admin.site.register(Bookmark, BookmarkAdmin)
