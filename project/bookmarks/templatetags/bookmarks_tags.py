from django import template
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import resolve, reverse
from django.template import loader

from ..models import Bookmark

register = template.Library()

@register.tag
def bookmark_widget(parser, token):
    """Inserts bookmark widget.

    If ajax=True, inserts a static widget that gets the initial bookmarked/not-bookmarked
    state via an AJAX call. This allows the page to be cached for multiple users, as
    the bookmark status is not in the HTML.

    If ajax=False, the bookmark status is calculated here; this saves an AJAX call
    but makes the page not cacheable across users.
    """

    tokens = token.split_contents()
    print(tokens)
    format_err = "{0} tag requires syntax: {{% {0} for <object> [ajax=<True|False>] %}}".format(tokens[0])

    try:
        if len(tokens) == 4:
            ajax_opt = tokens.pop()
            if ajax_opt == 'ajax':
                ajax = 'True'
            else:
                ajax_str, ajax = ajax_opt.split("=")
                if ajax_str != 'ajax':
                    raise ValueError
        else:
            ajax = "False"  # will get resolved as variable -> bool(False)

        tag_name, for_str, obj = tokens
        if for_str != 'for':
            raise ValueError

    except ValueError:
            raise template.TemplateSyntaxError(format_err)

    return ObjectBookmarkWidget(obj, ajax)


class ObjectBookmarkWidget(template.Node):
    def __init__(self, obj, ajax):
        self.obj = obj
        self.ajax = ajax

    def render(self, context):
        obj = template.resolve_variable(self.obj, context)
        ajax = template.resolve_variable(self.ajax, context)
        ct = ContentType.objects.get_for_model(obj)
        user = context['request'].user

        context.push()
        context['object'] = obj
        context['content_type_id'] = ct.pk

        kwargs = {'content_type_id': ct.pk, 'object_id': obj.pk}
        context['toggle_url'] = reverse('bookmarks:bookmark_toggle', kwargs=kwargs)
        context['get_url'] = reverse('bookmarks:bookmark_get', kwargs=kwargs)

        context['ajax'] = ajax
        if not ajax:
            context['bookmarked'] = Bookmark.is_bookmarked(user, ct.pk, obj.pk)

        output = loader.render_to_string("bookmarks/includes/bookmark.html", context)
        context.pop()

        return output
