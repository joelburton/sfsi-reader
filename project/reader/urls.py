"""Site URLs."""

from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

from .views import HomepageView, TestErrorView
from members.views import ProfileUpdateView

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^comments/', include('django_comments.urls')),
    url(r'^accounts/profile/', ProfileUpdateView.as_view(), name='account_profile'),
    url(r'^accounts/avatar/', 'avatar.views.add', name='account_avatar'),

    url(r'^accounts/', include('allauth.urls')),

    url(r'^members/', include('members.urls')),
    url(r'^$', HomepageView.as_view()),
    url(r'^_error/$', TestErrorView.as_view()),
    url(r'^', include('resources.urls', namespace='resources')),
    url(r'^avatar/', include('avatar.urls')),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)