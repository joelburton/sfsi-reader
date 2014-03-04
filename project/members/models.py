from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import permalink


class Semester(models.Model):
    """Semester of training."""

    title = models.CharField(
        max_length=20,
    )

    def __unicode__(self):
        return self.title


class Member(AbstractUser):
    """Site member."""

    semesters = models.ManyToManyField(
        Semester,
        blank=True,
    )

    description = models.CharField(
        max_length=250,
        blank=True,
        verbose_name='summary',
        help_text="A short sentence about who you are.",
    )

    body = models.TextField(
        blank=True,
        verbose_name='biography',
    )

    visible = models.BooleanField(
        default=False,
        help_text='Check this to make your profile visible to your fellow students.'
        ' Regardless, your email will never be shown to anyone but training staff.',
    )

    @permalink
    def get_absolute_url(self):
        return 'member.detail', (), {'slug': self.username}

    # class Meta(AbstractUser.Meta):
    #     verbose_name = 'member'
    #
    # objects = ZanaMemberManager()
