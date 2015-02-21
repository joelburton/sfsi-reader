from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views import generic
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import time

from .models import Bookmark


@require_POST
@login_required
@never_cache
@csrf_exempt
def bookmark_toggle(request, content_type_id, object_id):
    """Sets/unsets the objects as a bookmark for the current user."""

    bookmark, created = Bookmark.objects.get_or_create(
        content_type_id=content_type_id,
        object_id=object_id,
        user=request.user,
    )

    if created:
        return JsonResponse({'action': 'set'})

    if not created:
        bookmark.delete()
        return JsonResponse({'action': 'unset'})

@login_required
@never_cache
def bookmark_get(request, content_type_id, object_id):
    """Gets bookmark status for the current user."""

    is_set = Bookmark.objects.filter(
        content_type_id=content_type_id,
        object_id=object_id,
        user=request.user,
    ).exists()

    return JsonResponse({'set': is_set})


class BookmarksListView(generic.ListView):

    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user)