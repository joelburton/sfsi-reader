"""Views related to resources and searching resources."""
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail

from django.db import connection
from django.http import Http404
from django.views import generic

from .models import Day, Topic, Resource, Suggestion
from .forms import SuggestionForm


class DayListView(generic.ListView):
    """List of days."""

    def get_queryset(self):
        return Day.objects.active()


class DayDetailView(generic.DetailView):
    """Detail view of a day, listing topics for that day."""

    def breadcrumbs(self):
        return [('/days/', 'Days'),
                (self.object.get_absolute_url(), self.object.title)]

    def get_queryset(self):
        return Day.objects.active()

    def get_context_data(self, **kwargs):
        data = super(DayDetailView, self).get_context_data(**kwargs)
        data['topics'] = data['day'].topic_set.active().only(
            "title", "description", "id", "slug", "day"
        )
        return data


##################################################################################################


class TopicListView(generic.ListView):
    """List of all topics."""

    def get_queryset(self):
        return Topic.objects.active().order_by('title').prefetch_related("day").only(
            "title", "description", "id", "slug", "day"
        )


class TopicDetailView(generic.DetailView):
    """Detail view of a topic, listing resources for that topic."""

    context_object_name = 'topic'
    template_name = "resources/topic_detail.html"

    def breadcrumbs(self):
        return [('/days/', 'Days'),
                (self.object.day.get_absolute_url(), self.object.day.title),
                (self.object.get_absolute_url(), self.object.title)]

    def get_object(self, queryset=None):
        try:
            return Topic.objects.active().only(
                "title", "description", "id", "slug", "day"
            ).get(slug=self.kwargs['slug'], day__slug=self.kwargs['day_slug'])
        except Topic.DoesNotExist:
            raise Http404()

    def get_context_data(self, **kwargs):
        data = super(TopicDetailView, self).get_context_data(**kwargs)
        # Important: we don't want the massive search fields from resources pulled down!
        data['resources'] = data['topic'].resource_set.active().only(
            "title", "description", "id", "topic", "key", "required", "slug")
        data['topics'] = data['topic'].day.topic_set.active().order_by('title')
        return data


##################################################################################################


class KeyListView(generic.ListView):
    """List of key resources."""

    template_name = "resources/key_list.html"
    model = Resource

    def get_queryset(self):
        return Resource.objects.active().filter(key=True).only(
            "title", "description", "id", "topic", "key", "required", "slug"
        )


class RequiredListView(generic.ListView):
    """List of required resources."""

    model = Resource
    template_name = "resources/required_list.html"

    def get_queryset(self):
        return Resource.objects.active().filter(required=True).only(
            "title", "description", "id", "topic", "key", "required", "slug"
        )


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
        try:
            return Resource.objects\
                .active()\
                .defer("body")\
                .get(slug=self.kwargs['slug'],
                     topic__slug=self.kwargs['topic_slug'],
                     topic__day__slug=self.kwargs['day_slug'])
        except Resource.DoesNotExist:
            raise Http404()

    def get_context_data(self, **kwargs):
        data = super(ResourceDetailView, self).get_context_data(**kwargs)
        data['resources'] = data['resource'].topic.resource_set.active().order_by('title')
        return data


class AdditionalResourcesView(generic.DetailView):
    """Detail view of a resource."""

    template_name = "resources/resource_detail.html"
    context_object_name = "resource"

    def breadcrumbs(self):
        return [('/days/', 'Days'),
                (self.object.topic.day.get_absolute_url(), self.object.topic.day.title),
                (self.object.topic.get_absolute_url(), self.object.topic.title),
                (self.object.get_absolute_url(), self.object.title)]

    def get_object(self, queryset=None):
        try:
            return Resource.objects\
                .active()\
                .defer("body")\
                .get(is_more=True)
        except Resource.DoesNotExist:
            raise Http404()


##################################################################################################


class SearchView(generic.TemplateView):
    """Search form and results listing."""

    template_name = 'resources/search.html'

    def get_context_data(self, **kwargs):
        data = super(SearchView, self).get_context_data(**kwargs)
        data['q'] = q = self.request.GET.get('q', '')
        if q:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT title,"
                "       absolute_url,"
                "       ts_headline('english', title || ' ' || description, sterm) AS highlight,"
                "       ts_rank_cd(search, sterm) AS rank"
                " FROM resources_topic,"
                "      plainto_tsquery(%s) AS sterm"
                " WHERE sterm @@ search"
                "   AND status='published'"
                " ORDER BY rank DESC", [q]
            )
            data['topic_results'] = cursor.fetchall()

            cursor.execute(
                "SELECT title,"
                "       absolute_url,"
                "       ts_headline('english', title || ' ' || description || ' ' || file || "
                "                              ' ' || link || ' ' || body, sterm) AS highlight,"
                "       ts_rank_cd(search, sterm) AS rank"
                " FROM resources_resource,"
                "      plainto_tsquery(%s) AS sterm"
                " WHERE sterm @@ search"
                "   AND status='published'"
                " ORDER BY rank DESC", [q]
            )
            data['resource_results'] = cursor.fetchall()

        return data


##################################################################################################


MSG = """
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

    # def get_form_kwargs(self):
    #     """Supply initial arguments."""
    #     kw = super(SuggestionCreateView, self).get_form_kwargs()
    #     kw['initial']['name'] = self.request.user.get_full_name()
    #     kw['initial']['email'] = self.request.user.email
    #     return kw

    def get_initial(self):
        return {'name': self.request.user.get_full_name(),
                'email': self.request.user.email}

    def form_valid(self, form):

        send_mail("[Reader Suggestion] %s" % form.cleaned_data['title'],
                  MSG % form.cleaned_data,
                  form.cleaned_data['email'],
                  [x[1] for x in settings.MANAGERS],
                  fail_silently=False)

        messages.add_message(self.request, messages.SUCCESS, "Your suggestion has been noted.")
        return super(SuggestionCreateView, self).form_valid(form)