"""Administrative resources related to resources."""

from django import forms

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm

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

    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/js/tinymce_setup.js',
        ]


admin.site.register(Semester)

admin.site.register(Member, MemberAdmin)
