"""
Forms related to resources.
"""

from django import forms
from django.utils.text import slugify

from .models import Resource, Topic, Suggestion


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
            self.instance.index_file(self.cleaned_data['file'])
        if 'link' in self.changed_data:
            self.instance.index_link(self.cleaned_data['link'])
        return forms.ModelForm.save(self, commit)

    class Meta:
        model = Resource


class SuggestionForm(forms.ModelForm):
    """Suggestion form."""

    topic = forms.ChoiceField(
        choices=[('', '(select topic for resource'), ('other', '(Other)')],
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super(SuggestionForm, self).__init__(*args, **kwargs)
        self.fields['topic'].choices += [
            (t.title, t.title)
            for t in Topic.objects.active().order_by('title')
        ]

    class Meta:
        model = Suggestion