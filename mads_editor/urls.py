from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('fourstore.views',
    # Examples:
    # url(r'^$', 'mads_editor.views.home', name='home'),
    # url(r'^mads_editor/', include('mads_editor.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r"^sparql/$", "sparql_proxy", {"sparql_endpoint": "http://www.dbpedia.org/sparql/"}),
)
