"""Models related to resources."""

from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import permalink
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from docutils.parsers.rst.directives.body import Topic

from model_utils.models import TimeStampedModel, StatusModel


def make_published(modeladmin, request, queryset):
    """Action for administrative interface to publish."""

    for o in queryset.all():
        o.status = 'published'
        o.save()

make_published.short_description = 'Publish'


def make_private(modeladmin, request, queryset):
    """Action for administrative interface to hide things."""

    for o in queryset.all():
        o.status = 'private'
        o.save()

make_private.short_description = 'Make private'


##################################################################################################


class MetadataMixin(TimeStampedModel, StatusModel):
    """Base mixin class for all of our content types.

    Provides core metadata we want:

    - title
    - slug
    - description
    - absolute_url (used for search results)
    """

    # These are our workflow states; the first one is the default
    STATUS = [('published', 'Published'), ('private', 'Private')]

    title = models.CharField(
        max_length=70
    )

    slug = models.SlugField()

    description = models.TextField(
    )

    # Normally, it's slightly in bad taste to store the URL for an object--we'd let Django
    # calculate it. But to make search result rendering fast, we include it here, so the
    # search system can use it.

    absolute_url = models.CharField(
        max_length=100,
        )

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.title

    def is_active(self):
        """Is this item active?

        This is used in the administrative interface to show a green check if item published."""

        return self.status == 'published'
    is_active.boolean = True
    is_active.description = 'Active?'

    def save(self, **kwargs):
        """Capture the URL during item save."""

        self.absolute_url = self.get_absolute_url()
        super(MetadataMixin, self).save(**kwargs)


##################################################################################################


class PublishedManager(models.Manager):
    """Custom manager for showing published stuff."""

    use_for_related_fields = True

    def active(self):
        """List of items that should be active on site."""

        return self.filter(status='published')


##################################################################################################


class Day(MetadataMixin):
    """Training day."""

    class Meta:
        unique_together = [['slug'], ['title']]
        ordering = ['title']

    objects = PublishedManager()

    @permalink
    def get_absolute_url(self):
        return 'resources:day.detail', (), {'slug': self.slug}


##################################################################################################


class Topic(MetadataMixin):
    """Training topic. There are several topics in a day. Topics collect resources."""

    day = models.ForeignKey(Day)

    position = models.PositiveSmallIntegerField(
        default=0,
        help_text='Ordering position with the day.',
        )

    class Meta:
        # Topic slugs are unique across site. We don't *need* to have this be the case--topics
        # could be unique only within their day, for instance, but we're so unlikely to actually
        # have overlapping topic titles/slugs, it's far more likely to be user error.
        unique_together = [['slug'], ['title']]

        ordering = ['title']

    objects = PublishedManager()

    @permalink
    def get_absolute_url(self):
        return 'resources:topic.detail', (), {'day_slug': self.day.slug, 'slug': self.slug}


##################################################################################################


class Resource(MetadataMixin):
    """Resource.

    Resources are contained within topics. Resources can be either a link or a file; the same type
    is used for both.
    """

    topic = models.ForeignKey(Topic)

    link = models.URLField(
        blank=True,
        help_text='Full URL to an externally-hosted resource.',
        )

    file = models.FileField(
        blank=True,
        upload_to='resources',
        )

    file_size = models.PositiveIntegerField(
        blank=True,
        null=True,
        )

    file_mimetype = models.CharField(
        max_length=255,
        blank=True,
        )

    key = models.BooleanField(
        verbose_name='Key Resource?',
        default=False,
        )

    required = models.BooleanField(
        verbose_name='Required Reading?',
        default=False,
        )

    is_more = models.BooleanField(
        verbose_name='Additional Resources',
        help_text='Check if this is the resource that should show up as "additional resources"',
        default=False,
    )

    body = models.TextField(
        blank='',
        help_text='This is the extracted body of the PDF/remote link, used for searching.',
        )

    class Meta:
        # Resources are uniquely titled and slugged within their topic
        unique_together = [['topic', 'slug'], ['topic', 'title']]

        # We sort them with key resources first, followed by non-key; in both cases, by title
        index_together = [['key', 'title']]
        ordering = ['-key', 'title']

    objects = PublishedManager()

    @permalink
    def get_absolute_url(self):
        return 'resources:resource.detail', (), {'day_slug': self.topic.day.slug,
                                                 'topic_slug': self.topic.slug,
                                                 'slug': self.slug }

    def clean(self):
        """Validate model across fields."""

        if (self.file and self.link) or (not self.file and not self.link):
            raise ValidationError("Must have either a link or a file, but not both.")

        if self.is_more:
            others = Resource.objects.exclude(id=self.id).filter(is_more=True)
            if others:
                raise ValidationError("There can only be one 'Additional Resources' on site.")

        return super(Resource, self).clean()


##################################################################################################


class Suggestion(TimeStampedModel):
    """Suggestion for additional resource.
    """

    title = models.CharField(
        max_length=70
    )

    description = models.TextField(
    )

    topic = models.CharField(
        max_length=100,
    )

    name = models.CharField(
        max_length=100,
    )

    email = models.EmailField(
    )

    class Meta:
        ordering = ['-created']

