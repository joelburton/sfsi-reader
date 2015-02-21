from django import template
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

from ..models import Bookmark


register = template.Library()


@register.inclusion_tag('bookmarks/includes/bookmark.html', takes_context=True)
def bookmark_widget(context, obj, ajax=False):

    content_type_id = ContentType.objects.get_for_model(obj).pk
    obj_id = obj.pk
    user = context['request'].user

    # For ajax widget, we have it get the bookmark status via AJAX call
    bookmarked = None if ajax else Bookmark.is_bookmarked(user, content_type_id, obj_id)

    kwargs = {'content_type_id': content_type_id, 'object_id': obj_id}
    toggle_url = reverse('bookmarks:bookmark_toggle', kwargs=kwargs)
    get_url = reverse('bookmarks:bookmark_get', kwargs=kwargs)

    return {
        'content_type_id': content_type_id,
        'toggle_url': toggle_url,
        'get_url': get_url,
        'ajax': ajax,
        'bookmarked': bookmarked
    }
