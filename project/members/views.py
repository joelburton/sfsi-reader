from django.contrib import messages
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.generic import UpdateView
from members.forms import MemberProfileForm
from members.models import Member


class MemberListView(generic.TemplateView):
    """List of members in your semester."""

    template_name = 'members/member_list.html'

    def get_context_data(self, **kwargs):
        data = super(MemberListView, self).get_context_data(**kwargs)
        data['semesters'] = []
        for semester in self.request.user.semesters.all():
            data['semesters'].append(
                {'title': semester.title,
                 'students': [m
                              for m
                              in Member.objects.filter(semesters=semester, visible=True).order_by('last_name', 'first_name')],
                }
            )
        return data


class MemberDetailView(generic.DetailView):
    """Profile page for a member."""

    slug_field = 'username'

    def breadcrumbs(self):
        return [('/members/', 'Members'),
                (self.object.get_absolute_url(), self.object.get_full_name())]

    def get_queryset(self):
        user_semesters = self.request.user.semesters.all()
        return Member.objects.filter(semesters=user_semesters, visible=True)


class ProfileUpdateView(UpdateView):
    """Update logged-in user profile."""

    model = Member
    form_class = MemberProfileForm
    template_name = 'account/profile.html'
    success_url = '/accounts/profile/'

    def get_object(self):
        """Get the currently logged-in user."""

        return self.request.user

    def form_valid(self, form):
        url = reverse('member.detail', kwargs={'slug': self.request.user.username})
        messages.add_message(self.request,
                             messages.SUCCESS,
                             'Profile edited. <a href="%s">View your profile</a>' % url)
        return super(self.__class__, self).form_valid(form)

