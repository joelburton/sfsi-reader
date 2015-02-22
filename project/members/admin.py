"""Administrative resources related to resources."""

from django import forms
from django.contrib.admin import ModelAdmin
from django.forms import widgets
from django.db import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm

from tinymce.widgets import TinyMCE

from .models import Semester, Member


class MemberAdminCreationForm(UserCreationForm):
    """We need to subclass this because the original always used the "User" model."""

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            Member._default_manager.get(username=username)
        except Member.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    class Meta(UserCreationForm.Meta):
        model = Member


@admin.register(Member)
class MemberAdmin(UserAdmin):
    add_form = MemberAdminCreationForm
    fieldsets = UserAdmin.fieldsets + (
        ('Profile', {
            'fields': ('description',
                       'body',
                       'visible',
                       'semesters',
            )
        }),
    )

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE},
        models.ManyToManyField: {'widget': widgets.CheckboxSelectMultiple}
    }

    def get_form(self, request, obj=None, **kwargs):
        """Don't show add-new button for semesters field."""

        form = super(MemberAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['semesters'].widget.can_add_related = False
        return form


@admin.register(Semester)
class SemesterAdmin(ModelAdmin):
    pass
