from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mads_editor.views.home', name='home'),
    # url(r'^mads_editor/', include('mads_editor.foo.urls')),

    url(r"^$", 'mads_editor.search.search'),
    url(r"^new$", 'mads_editor.resource.new'),
    url(r"^([a-zA-Z0-9_]+)/$", 'mads_editor.resource.resource'),
    url(r"^([a-zA-Z0-9_]+)$", 'mads_editor.resource.resource'),

)
