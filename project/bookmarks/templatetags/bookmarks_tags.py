from django import template
from django.contrib.contenttypes.models import ContentType
from django.template import loader

from ..models import Bookmark

register = template.Library()

@register.tag
def bookmark_widget(parser, token):
    tokens = token.split_contents()
    format_err = "{0} tag requires syntax: {{% {0} for <object> %}}".format(tokens[0])

    try:
        tag_name, for_str, obj = tokens
    except ValueError:
        raise template.TemplateSyntaxError(format_err)

    if for_str != 'for':
        raise template.TemplateSyntaxError(format_err)

    return ObjectBookmarkWidget(obj)


class ObjectBookmarkWidget(template.Node):
    def __init__(self, obj):
        self.obj = obj

    def render(self, context):
        obj = template.resolve_variable(self.obj, context)
        ct = ContentType.objects.get_for_model(obj)
        user = context['request'].user

        context.push()
        context['object'] = obj
        context['content_type_id'] = ct.pk
        context['is_bookmarked_by_user'] = Bookmark.is_bookmarked(user, ct.pk, obj.pk)

        output = loader.render_to_string("bookmarks/includes/bookmark.html", context)
        context.pop()

        return output
