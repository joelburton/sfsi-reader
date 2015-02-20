"""URLs related to resources:

/members/
  List of people in your semesters.

/members/[username]
  Public profile.
"""

from django.conf.urls import url

from .views import MemberListView, MemberDetailView, MemberBulkAddView, MemberBulkAddSuccessView


urlpatterns = [

    url(r'^semester-add/$',
        MemberBulkAddView.as_view(),
        name='member.bulkadd'),

    url(r'^semester-add/success/$',
        MemberBulkAddSuccessView.as_view(),
        name='member.bulkadd-success'),

    url(r'^$',
        MemberListView.as_view(),
        name='member.list'),

    url(r'^(?P<slug>[^/]+)/$',
        MemberDetailView.as_view(),
        name='member.detail'),

]
