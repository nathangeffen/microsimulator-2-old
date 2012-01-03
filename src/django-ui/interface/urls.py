from django.conf.urls.defaults import patterns, include, url
from django.views.generic import TemplateView
from django.conf import settings


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/', include('registration.urls')),
    url(r'^$', TemplateView.as_view(template_name="index.html"),name="home"),
    (r'^specification/', include('specification.urls')),   
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^grappelli/', include('grappelli.urls')),  
    url(r'^admin/', include(admin.site.urls)),      
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
