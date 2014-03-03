"""URLs related to resources:

/members/
  List of people in your semesters.

/members/[username]
  Public profile.
"""

from django.conf.urls import patterns, url
from members.views import MemberListView, MemberDetailView


urlpatterns = patterns(
    '',

    url(r'^$',
        MemberListView.as_view(),
        name='member.list'),

    url(r'^(?P<slug>[^/]+)/$',
        MemberDetailView.as_view(),
        name='member.detail'),

)
