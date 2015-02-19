"""Views related to resources and searching resources."""

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.db import connection
from django.shortcuts import get_object_or_404
from django.views import generic

from .models import Day, Topic, Resource, Suggestion
from .forms import SuggestionForm


class DayListView(generic.ListView):
    """List of days."""

    queryset = Day.objects.active()


class DayDetailView(generic.DetailView):
    """Detail view of a day, listing topics for that day."""

    queryset = Day.objects.active()

    def breadcrumbs(self):
        return [('/days/', 'Days'),
                (self.object.get_absolute_url(), self.object.title)]

    def get_context_data(self, **kwargs):
        """Get topics for this day."""

        context = super(DayDetailView, self).get_context_data(**kwargs)
        context['topics'] = context['day'].topic_set.active().order_by('position')
        return context


##################################################################################################


class TopicListView(generic.ListView):
    """List of all topics."""

    queryset = Topic.objects.active().prefetch_related("day")


class TopicDetailView(generic.DetailView):
    """Detail view of a topic, listing resources for that topic."""

    context_object_name = 'topic'
    template_name = "resources/topic_detail.html"

    def breadcrumbs(self):
        return [('/days/', 'Days'),
                (self.object.day.get_absolute_url(), self.object.day.title),
                (self.object.get_absolute_url(), self.object.title)]

    def get_object(self, queryset=None):
        return get_object_or_404(
            Topic.objects.active(),
            slug=self.kwargs['slug'],
            day__slug=self.kwargs['day_slug'],
        )

    def get_context_data(self, **kwargs):
        """Get resources and other-topics-in-this-day."""

        context = super(TopicDetailView, self).get_context_data(**kwargs)
        # Important: we don't want the massive search fields from resources pulled down!
        context['resources'] = context['topic'].resource_set.active().defer("body")
        context['topics'] = context['topic'].day.topic_set.active()
        return context


##################################################################################################


class KeyListView(generic.ListView):
    """List of key resources."""

    template_name = "resources/key_list.html"

    queryset = Resource.objects.active().filter(key=True) \
        .defer("body") \
        .prefetch_related('topic', 'topic__day') \
        .order_by('topic', 'title')


class RequiredListView(generic.ListView):
    """List of required resources."""

    template_name = "resources/required_list.html"

    queryset = Resource.objects.active().filter(required=True) \
        .defer("body") \
        .prefetch_related('topic', 'topic__day') \
        .order_by('topic', 'title')


class ResourceDetailView(generic.DetailView):
    """Detail view of a resource."""

    template_name = "resources/resource_detail.html"
    context_object_name = "resource"

    def breadcrumbs(self):
        return [('/days/', 'Days'),
                (self.object.topic.day.get_absolute_url(), self.object.topic.day.title),
                (self.object.topic.get_absolute_url(), self.object.topic.title),
                (self.object.get_absolute_url(), self.object.title)]

    def get_object(self, queryset=None):
        return get_object_or_404(
            Resource.objects.active().defer("body"),
            slug=self.kwargs['slug'],
            topic__slug=self.kwargs['topic_slug'],
            topic__day__slug=self.kwargs['day_slug'])

    def get_context_data(self, **kwargs):
        """Get other resources in this topic."""

        context = super(ResourceDetailView, self).get_context_data(**kwargs)
        context['resources'] = context['resource'].topic.resource_set.active().order_by('title')
        return context


class AdditionalResourcesView(ResourceDetailView):
    """Detail view of the resource that is the "more resources" link."""

    def get_object(self, queryset=None):
        return get_object_or_404(
            Resource.objects.active().defer("body"),
            is_more=True
        )


##################################################################################################


class SearchView(generic.TemplateView):
    """Search form and results listing."""

    template_name = 'resources/search.html'

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context['q'] = q = self.request.GET.get('q', '')
        if q:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT title,"
                "       absolute_url,"
                "       description,"
                "       ts_headline('english', title || ' ' || description, sterm) AS highlight,"
                "       ts_rank_cd(search, sterm) AS rank"
                " FROM resources_topic,"
                "      plainto_tsquery(%s) AS sterm"
                " WHERE sterm @@ search"
                "   AND status='published'"
                " ORDER BY rank DESC", [q]
            )
            context['topic_results'] = cursor.fetchall()

            cursor.execute(
                "SELECT title,"
                "       absolute_url,"
                "       description,"
                "       ts_headline('english', title || ' ' || description || ' ' || file || "
                "                              ' ' || link || ' ' || body, sterm) AS highlight,"
                "       ts_rank_cd(search, sterm) AS rank"
                " FROM resources_resource,"
                "      plainto_tsquery(%s) AS sterm"
                " WHERE sterm @@ search"
                "   AND status='published'"
                " ORDER BY rank DESC", [q]
            )
            context['resource_results'] = cursor.fetchall()

        return context


##################################################################################################


SUGGESTION_MSG = """
A new resource has been suggested for the reader.

Name: %(name)s
Email: %(email)s
Title: %(title)s
Description: %(description)s

Please visit the reader to view this resource.
"""


class SuggestionCreateView(generic.CreateView):
    """Create view for suggestions."""

    model = Suggestion
    form_class = SuggestionForm
    success_url = "/"

    def get_initial(self):
        """Initially fill with user info."""

        return {'name': self.request.user.get_full_name(),
                'email': self.request.user.email}

    def form_valid(self, form):
        """Send email and thank user."""

        send_mail("[Reader Suggestion] %s" % form.cleaned_data['title'],
                  SUGGESTION_MSG % form.cleaned_data,
                  "joel@joelburton.com",
                  [mgr[1] for mgr in settings.MANAGERS],
                  fail_silently=False)

        messages.add_message(self.request, messages.SUCCESS, "Your suggestion has been noted.")
        return super(SuggestionCreateView, self).form_valid(form)
