"""Models related to resources."""

from __future__ import unicode_literals
import urllib2

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import permalink
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from docutils.parsers.rst.directives.body import Topic

from model_utils.models import TimeStampedModel, StatusModel
from resources.pdfconvert import convert_pdf_to_txt


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
        max_length=100
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

    def index_file(self, file, mimetype=None, size=None):
        """Read contents of file and update metadata."""

        if file:
            self.file_mimetype = mimetype if mimetype is not None else file.content_type
            self.file_size = size if size is not None else file.size
            if self.file_mimetype.endswith('/pdf'):
                try:
                    self.body = convert_pdf_to_txt(file)
                except Exception:
                    raise
                    # I'm uncertain what errors the converter might throw, but it's better to
                    # allow unread PDFs than raise errors on conversion, so we'll be a little
                    # overly broad here.
                    self.body = ''
            else:
                self.body = ''
        else:
            # Switched from file-based to URL-based, clear out this stuff
            self.file_size = 0
            self.file_mimetype = ''

    def index_link(self, link):
        """Read contents of link and update metadata."""

        if link:
            try:
                http_obj = urllib2.urlopen(link, timeout=10)
                self.body = http_obj.read().decode('utf8')
            except (urllib2.URLError, UnicodeDecodeError):
                # Again, better to get something than nothing
                self.body = ''


##################################################################################################


class Suggestion(TimeStampedModel):
    """Suggestion for additional resource.
    """

    title = models.CharField(
        max_length=70,
        verbose_name='subject',
    )

    description = models.TextField(
        help_text='Describe the suggested resource.',
        blank=True,
    )

    topic = models.CharField(
        max_length=100,
        blank=True,
    )

    # We don't want to confuse people who paste an invalid URL, so let's be very forgiving and
    # use a CharField here
    link = models.CharField(
        help_text='For web-based resources, please paste the URL here.',
        blank=True,
        max_length=200,
    )

    file = models.FileField(
        help_text='For file-based resources, please upload the file here.',
        upload_to='suggestions',
        blank=True,
    )

    name = models.CharField(
        max_length=100,
        verbose_name='your name',
        blank=True,
        help_text="If you'd like your submission to be confidential, you can clear this."
    )

    email = models.EmailField(
        verbose_name='your email',
        blank=True,
        help_text="If you'd like your submission to be confidential, you can clear this.",
    )

    class Meta:
        ordering = ['-created']

    def __unicode__(self):
        return self.title

