"""urly_bird URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import login
from bookmark.views import Bookmark, BookmarkCreate, BookmarkDelete, BookmarkUpdate, BookmarkListView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TemplateView.as_view(
        template_name="index.html"),
        name='index'),
    url(r'^register/', CreateView.as_view(
            template_name='register.html',
            form_class=UserCreationForm,
            success_url='index'),
            name='user_register'),
    url(r'^accounts/', include('django.contrib.auth.urls')),  # FIXME: Make a lost password template
    url(r'^login/$', login, name='login'),
    # url(r'^logout', django.contrib.auth.logout(request)),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
    {'next_page': '/'}), # FIXME: Make this a non-admin view
    url(r'^bookmarks/$', BookmarkListView.as_view(), name="bookmark_list"),

    url(r'bookmark/add/$', BookmarkCreate.as_view(), name='bookmark_add'),
    url(r'bookmark/(?P<pk>[A-Za-z0-9]+)/$', BookmarkUpdate.as_view(), name='bookmark_update'),
    url(r'bookmark/(?P<pk>[A-Za-z0-9]+)/delete/$', BookmarkDelete.as_view(), name='bookmark_delete'),
    url(r'bookmark/detail/(?P<pk>[A-Za-z0-9]+)/$', BookmarkUpdate.as_view(), name='bookmark_detail'), # FIXME: Redundant, add loginrequired

]


