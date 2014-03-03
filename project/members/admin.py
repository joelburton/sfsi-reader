"""Administrative resources related to resources."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from members.models import Semester, Member


class MemberAdmin(UserAdmin):
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
