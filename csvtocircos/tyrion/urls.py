from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'tyrion.views.home', name='home'),
    url(r'^circos/(?P<title>.+)/', 'tyrion.views.showGraph'),
    url(r'^proc/', 'tyrion.views.proc'),
    url(r'^updateGraph', 'tyrion.views.updateGraph'),
    # url(r'^tyrion/', include('tyrion.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
