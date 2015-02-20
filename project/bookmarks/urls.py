from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<content_type_id>[^/]+)/(?P<object_id>[^/]+)/$',
        views.bookmark_toggle,
        name='bookmark_toggle'),

    url(r'^$',
        views.BookmarksListView.as_view(),
        name='bookmark_list'),

]