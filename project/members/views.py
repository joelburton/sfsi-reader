import smtplib

from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic import UpdateView, FormView, TemplateView
from django.contrib.admin.views.decorators import staff_member_required

from .forms import MemberProfileForm, SemesterBulkCreationForm, \
    MemberBulkCreationFormSet
from .models import Member


class MemberListView(generic.TemplateView):
    """List of members in your semester."""

    template_name = 'members/member_list.html'

    def get_context_data(self, **kwargs):
        """Show visible peers from their semesters."""

        context = super(MemberListView, self).get_context_data(**kwargs)
        context['semesters'] = []
        for semester in self.request.user.semesters.all():
            peers = (Member.objects
                     .filter(semesters=semester, visible=True)
                     .order_by('last_name', 'first_name'))
            context['semesters'].append({'title': semester.title, 'students': list(peers)})
        return context


class MemberDetailView(generic.DetailView):
    """Profile page for a member."""

    slug_field = 'username'

    def breadcrumbs(self):
        return [('/members/', 'Members'),
                (self.object.get_absolute_url(), self.object.get_full_name())]

    def get_queryset(self):
        """Students can see themselves and their peers from their semester(s)."""

        user_semesters = self.request.user.semesters.all()
        if self.kwargs['slug'] == self.request.user.username:
            return Member.objects.filter(username=self.request.user.username)
        else:
            return Member.objects.filter(semesters=user_semesters, visible=True)

    def get_context_data(self, **kwargs):
        """Students can edit themselves."""

        context = super(MemberDetailView, self).get_context_data(**kwargs)
        context['editable'] = (self.kwargs['slug'] == self.request.user.username)
        return context


class ProfileUpdateView(UpdateView):
    """Update logged-in user profile."""

    model = Member
    form_class = MemberProfileForm
    template_name = 'account/profile.html'
    success_url = '/accounts/profile/'

    def get_object(self, queryset=None):
        """Get the currently logged-in user."""

        return self.request.user

    def form_valid(self, form):
        url = self.object.get_absolute_url()
        messages.add_message(self.request,
                             messages.SUCCESS,
                             'Profile edited. <a href="%s">View your profile</a>' % url)
        return super(self.__class__, self).form_valid(form)


class MemberBulkAddView(FormView):
    """Add members for a semester."""

    form_class = SemesterBulkCreationForm
    template_name = 'members/member_bulkaddform.html'
    success_url = '/members/semester-add/success/'

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(MemberBulkAddView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Get member formset."""

        context = super(MemberBulkAddView, self).get_context_data(**kwargs)
        if self.request.method == "POST":
            context['member_form'] = MemberBulkCreationFormSet(self.request.POST)
        else:
            context['member_form'] = MemberBulkCreationFormSet()

        return context

    def form_valid(self, form):
        """Form (and formset of members) was valid; add them and send emails."""

        semester = form.cleaned_data['semester']
        password = form.cleaned_data['default_password']
        email_body = form.cleaned_data['email_body']

        member_form = MemberBulkCreationFormSet(self.request.POST)

        associated = []
        added = []
        errors = []

        for data in member_form.cleaned_data:
            if not data:
                continue

            fn, ln, email = data['first_name'], data['last_name'], data['email']
            data['password'] = password

            try:
                # Add this semester to an existing-in-system student
                member = Member.objects.get(email=email)
                member.semesters.add(semester)
                member.save()  # FIXME: do we need this for m2m-only changes?
                associated.append(data)

            except Member.DoesNotExist:
                # Add new student and send them welcome email
                username = (fn + "_" + ln).lower()
                member = Member.objects.create_user(username=username,
                                                    email=email,
                                                    password=password)
                member.semesters = [semester]
                member.first_name = fn
                member.last_name = ln
                member.save()
                added.append(data)

                try:
                    member.email_user(subject="SFSI Reader Login",
                                      message=email_body.format(**data),
                                      from_email='joel@joelburton.com')
                except smtplib.SMTPException:
                    errors.append(data)

        self.request.session['added'] = added
        self.request.session['associated'] = associated
        self.request.session['errors'] = errors

        return super(MemberBulkAddView, self).form_valid(form)


class MemberBulkAddSuccessView(TemplateView):
    """Report successful bulk add."""

    template_name = 'members/member_bulkaddform_success.html'

    def get_context_data(self, **kwargs):
        """Get status stuff and clear from session."""

        context = super(MemberBulkAddSuccessView, self).get_context_data(**kwargs)
        context['added'] = self.request.session['added']
        context['errors'] = self.request.session['errors']
        context['associated'] = self.request.session['associated']
        del self.request.session['added']
        del self.request.session['errors']
        del self.request.session['associated']
        return context



