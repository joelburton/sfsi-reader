from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Bookmark(models.Model):
    """User <-> content."""

    created = models.DateTimeField(
        auto_now_add=True,
        null=False
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
    )

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return "{0.user} bookmarked {0.content_object}".format(self)

    @classmethod
    def is_bookmarked(cls, user, content_type_id, pk):
        if user.is_authenticated():
            return cls.objects.filter(user=user,
                                      content_type_id=content_type_id,
                                      object_id=pk).exists()
        else:
            return False
