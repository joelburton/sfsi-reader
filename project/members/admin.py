"""Administrative resources related to resources."""

from django import forms
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
        models.TextField: {'widget':TinyMCE}
    }

    class Media:
        js = ('http://tinymce.cachefly.net/4.1/tinymce.min.js',)


admin.site.register(Semester)

admin.site.register(Member, MemberAdmin)
