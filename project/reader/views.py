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

    @staticmethod
    def latest_resources():
        """List of most recent resources created within 30 days."""

        start_date = datetime.datetime.now() - datetime.timedelta(days=300)
        return (Resource.objects
                .active()
                .only('title', 'topic_id', 'id', 'slug')
                .filter(created__gt=start_date)
                .select_related("topic", "topic__day")
                .order_by("-created")[:4]
        )

    def show_students(self):
        """Should we show link to other students in this semester?"""

        return self.request.user.semesters.exists()

    @staticmethod
    def comment_list():
        """Show 4 most recent comments by date."""

        return Comment.objects.order_by("-submit_date")[:4]


class TestErrorView(generic.View):
    """Test error page."""

    @staticmethod
    def get(request):
        raise Exception("Darn")