from django import forms
from django.forms import Textarea, formset_factory

from .models import Member, Semester


class MemberProfileForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = [
            'first_name',
            'last_name',
            'visible',
            'email',
            'description',
            'body',
        ]


class MemberBulkCreationForm(forms.Form):
    first_name = forms.CharField(max_length=20, required=True)
    last_name = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(max_length=75, required=True)


EMAIL_DEFAULT = """Dear {first_name} --

We have created an account for you for the SFSI Reader.

http://reader.sfsi.org

username: {email}
password: {password}

If you have problems signing in or using the site, please let us know.
Our technical support contact is joel@sfsi.org.

Thanks!

SFSI Training Staff"""


class SemesterBulkCreationForm(forms.Form):
    semester = forms.ModelChoiceField(Semester.objects.all())
    default_password = forms.CharField(max_length=20, required=True, initial="yaysexed")
    email_body = forms.CharField(widget=Textarea({'rows': 17, 'cols': 40}), initial=EMAIL_DEFAULT)

MemberBulkCreationFormSet= formset_factory(MemberBulkCreationForm, extra=40)