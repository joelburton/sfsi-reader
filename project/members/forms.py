from django import forms

from .models import Member


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