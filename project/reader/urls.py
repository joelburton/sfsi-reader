"""Site URLs."""

from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

from django.contrib import admin

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', TemplateView.as_view(template_name='homepage.html')),
    url(r'^', include('resources.urls', namespace='resources'))
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)