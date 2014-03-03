"""
Forms related to resources.
"""

import urllib2

from django import forms
from django.utils.text import slugify

from .models import Resource, Topic, Suggestion
from .pdfconvert import convert_pdf_to_txt


class TopicInlineForm(forms.ModelForm):
    """Topic form.

    Used when topics are inlined.
    """

    def save(self, commit=True):
        """Save. Calculates the slug since it's not on the form."""

        self.instance.slug = slugify(self.cleaned_data['title'])
        return forms.ModelForm.save(self, commit)

    class Meta:
        model = Topic


class ResourceForm(forms.ModelForm):
    """Resource form.

    When saving form, extract attributes of the uploaded file and, if PDF, read text into the
    body field.
    """

    def save(self, commit=True):
        if 'file' in self.changed_data:
            file = self.cleaned_data['file']
            if file:
                self.instance.file_mimetype = file.content_type
                self.instance.file_size = file.size
                if file.content_type.endswith('/pdf'):
                    try:
                        self.instance.body = convert_pdf_to_txt(file)
                    except Exception:
                        # I'm uncertain what errors the converter might throw, but it's better to
                        # allow unread PDFs than raise errors on conversion, so we'll be a little
                        # overly broad here.
                        self.instance.body = ''
                else:
                    self.instance.body = ''
            else:
                # Switched from file-based to URL-based, clear out this stuff
                self.instance.file_size = 0
                self.instance.file_mimetype = ''
        if 'link' in self.changed_data and self.cleaned_data['link']:
            try:
                http_obj = urllib2.urlopen(self.cleaned_data['link'], timeout=10)
                self.instance.body = http_obj.read()
            except urllib2.URLError:
                # Again, better to get something than nothing
                self.instance.body = ''

        return forms.ModelForm.save(self, commit)

    class Meta:
        model = Resource


class SuggestionForm(forms.ModelForm):
    """Suggestion form."""

    topic = forms.ChoiceField(
        choices=[('', '(select topic you think this would fall into')]
    )

    def __init__(self, *args, **kwargs):
        super(SuggestionForm, self).__init__(*args, **kwargs)
        self.fields['topic'].choices += [
            (t.title, t.title)
            for t in Topic.objects.active().order_by('title')
        ]

    class Meta:
        model = Suggestion
        fields = ['title', 'description', 'topic', 'name', 'email']