"""
Views for site.
"""
import datetime

from django.views import generic
from django_comments import Comment

from resources.models import Resource


class HomepageView(generic.TemplateView):
    """Homepage."""

    template_name = "homepage.html"

    def get_context_data(self, **kwargs):
        data = super(HomepageView, self).get_context_data()

        start_date = datetime.datetime.now() - datetime.timedelta(days=30)
        data['comment_list'] = Comment.objects\
                                   .order_by("-submit_date")[:4]
        data['latest_resources'] = Resource.objects\
                                       .active()\
                                       .filter(created__gt=start_date)\
                                       .order_by("-created")[:4]

        return data


class TestErrorView(generic.View):
    """Test error page."""

    def get(self, request):
        raise Exception("Darn")