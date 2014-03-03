"""URLs related to resources:

/days/
  List of all days

/days/day-[n]/
  List of topics for a day

/days/day-[n]/[topic-slug]/
  Topic detail page

/days/day-[n]/[topic-slug]/[resource-slug]/
  Resource detail page

/topics/
  List of all topics, across all days

/required/
  List of all required resources

/key-resources/
  List of all key resources

/more/
  Redirects to "more" resource page

/search/
  Search form/results

"""

from django.conf.urls import patterns, url

from .views import DayDetailView, DayListView, TopicDetailView, TopicListView, ResourceDetailView,\
    RequiredListView, KeyListView, SearchView, AdditionalResourcesView, SuggestionCreateView


urlpatterns = patterns(
    '',

    url(r'^days/$',
        DayListView.as_view(),
        name='day.list'),

    url(r'^days/(?P<slug>[^/]+)/$',
        DayDetailView.as_view(),
        name='day.detail'),

    url(r'^days/(?P<day_slug>[^/]+)/(?P<slug>[^/]+)/$',
        TopicDetailView.as_view(),
        name='topic.detail'),

    url(r'^days/(?P<day_slug>[^/]+)/(?P<topic_slug>[^/]+)/(?P<slug>[^/]+)/$',
        ResourceDetailView.as_view(),
        name='resource.detail'),

    url(r'^topics/$',
        TopicListView.as_view(),
        name='topic.list'),

    url(r'^required/$',
        RequiredListView.as_view(),
        name='topic.list'),

    url(r'^key-resources/$',
        KeyListView.as_view(),
        name='topic.list'),

    url(r'^more/$',
        AdditionalResourcesView.as_view(),
        name='search'),

    url(r'^search/$',
        SearchView.as_view(),
        name='search'),

    url(r'^suggestions/$',
        SuggestionCreateView.as_view(),
        name='suggestions'),
    )
