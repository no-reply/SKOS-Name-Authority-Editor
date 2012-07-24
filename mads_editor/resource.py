from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.conf import settings
from django.forms import Form, CharField, BooleanField
from django.forms.formsets import formset_factory, BaseFormSet
from SPARQLWrapper import SPARQLWrapper, JSON, N3
import urllib2
from query import QueryManager
from rdflib import URIRef
from rdflib import Namespace
from rdflib import Literal
from namespaces import Ns
import pynoid

namespaces = Ns.namespaces
ns = namespaces

def resource(request, ref=None):
    saved = False # set saved to false until post is successful
    uri = Namespace("http://data.library.oregonstate.edu/person/")[ref]
    endpoint = SPARQLWrapper(settings.ENDPOINT)
    endpoint.setReturnFormat(JSON)

    # check if our item exists
    query = "ASK { <%s> ?p ?o . }" % uri
    endpoint.setQuery(query)
    test = endpoint.query().convert()
    # deal with updates if this is a form submit
    if request.method == 'POST' and test['boolean'] == True:
        # get data to delete
        query = "DESCRIBE <%s>" % uri
        endpoint.setQuery(query)
        r = endpoint.query().convert()[str(uri)]
        
        # get form data and put it in a dict
        resForm = ResourceForm(request.POST)
        VariantFormSet = formset_factory(VariantForm)
        varForm = VariantFormSet(request.POST)
        if resForm.is_valid() and varForm.is_valid():
            data = {
                'res': resForm.cleaned_data,
                'var': varForm.cleaned_data
                }
            saved = processForm(uri, data, r)

    # if the uri exists, try to describe it and build an edit form 
    # retrieving data again if we just processed a form
    if test['boolean'] == True:
        query = "DESCRIBE <%s>" % uri
        endpoint.setQuery(query)
        r = endpoint.query().convert()[str(uri)]
        forms = buildForm(r)
    else:
        return HttpResponse("resource not found", status=404) #TODO: return a useful error

    return render_to_response("resource.tpl", {'uri': str(uri), 'short': uri.split('/')[-1], 'res': r, 'form': forms['form'], 'variants': forms['variants'], 'saved': saved})

def new(request, ref=None):
    test = {'boolean': True}
    while test['boolean'] == True:
        # assign an identifier
        identifier = pynoid.mint('zeek', random.randint(0, 100000))
        uri = Namespace("http://data.library.oregonstate.edu/person/")[identifer]
        endpoint = SPARQLWrapper(settings.ENDPOINT)
        endpoint.setReturnFormat(JSON)
        # check if an item aleady has this identifier
        query = "ASK { <%s> ?p ?o . }" % uri
        endpoint.setQuery(query)
        test = endpoint.query().convert()
    
    return HttpResponse(identifier, status=404) #TODO: return a useful error

def confirm(request, ref=None):
    #TODO: add confirmation step to form submit
    pass

def buildForm(resource):
    fields = {'name': resource[str(ns['skos']['prefLabel'])][0]['value']}
    #TODO: find better way to make empty form fields when there is no data
    try:
        fields['firstName'] = resource[str(ns['foaf']['givenName'])][0]['value'] 
    except:
        pass
    try:
        fields['lastName']= resource[str(ns['foaf']['familyName'])][0]['value']
    except:
        pass

    altLabel = str(ns['skos']['altLabel'])
    hiddenLabel = str(ns['skos']['hiddenLabel'])
    initial = []

    if (altLabel in resource) or (hiddenLabel in resource):
        try:
            for variant in resource[altLabel]:
                initial.append({'variant':variant['value'], 'isHidden':False})
        except:
            pass
        try:
            for variant in resource[hiddenLabel]:
                initial.append({'variant':variant['value'], 'isHidden':True})
        except:
            pass
        VariantFormSet = formset_factory(VariantForm, extra=0, formset=BaseVariantFormSet)
    else:
        VariantFormSet = formset_factory(VariantForm, extra=1, formset=BaseVariantFormSet)
    variantForm =  VariantFormSet(initial = initial)
    
    form = ResourceForm(fields)
    return {'form':form, 'variants':variantForm}


def processForm(uri, data, olddata):
    # not using SPARQLwrapper because update endpoints don't seem to work
    endpoint = settings.UPDATE
    #TODO: is there a good way to move all term matching to a single configurable location?
    terms={}
    rterms={}
    terms[ns['foaf']['familyName']] = data['res']['lastName']
    terms[ns['foaf']['givenName']] = data['res']['firstName']
    terms[ns['skos']['prefLabel']] = data['res']['name']
    rterms[ns['skos']['altLabel']] = []
    rterms[ns['skos']['hiddenLabel']] = []
    for label in data['var']:
        try:
            if label['isHidden']:
                rterms[ns['skos']['hiddenLabel']].append(label['variant'])
            else:
                rterms[ns['skos']['altLabel']].append(label['variant'])
        except:
            continue

    #TODO: make delete make sense
    delete = "DELETE DATA {" 
    try:
        for alt in olddata[str(ns['skos']['altLabel'])]:
            delete += "<%(uri)s> <http://www.w3.org/2004/02/skos/core#altLabel> '%(alt)s' . " % {'uri': uri, 'alt': alt['value']}
    except:
        pass
    try:
        for hidden in olddata[str(ns['skos']['hiddenLabel'])]:
            delete += "<%(uri)s> <http://www.w3.org/2004/02/skos/core#hiddenLabel> '%(hid)s' . " % {'uri': uri, 'hid': hidden['value']}
    except:
        pass

    try:
        for pref in olddata[str(ns['skos']['prefLabel'])]:
            delete += "<%(uri)s> <http://www.w3.org/2004/02/skos/core#prefLabel> '%(alt)s' . " % {'uri': uri, 'alt': pref['value']}
            delete += "<%(uri)s> <http://www.w3.org/2004/02/skos/core#label> '%(alt)s' . " % {'uri': uri, 'alt': pref['value']}
    except:
        pass
    try:
        for first in olddata[str(ns['foaf']['givenName'])]:
            delete += "<%(uri)s> <http://xmlns.com/foaf/0.1/givenName> '%(alt)s' . " % {'uri': uri, 'alt': first['value']}
    except:
        pass
    try:
        for last in olddata[str(ns['foaf']['familyName'])]:
            delete += "<%(uri)s> <http://xmlns.com/foaf/0.1/familyName> '%(alt)s' . " % {'uri': uri, 'alt': last['value']}
    except:
        pass
    delete += '}'

    # Insert Updated data
    update = 'INSERT DATA {'
    for term in terms:
        update += '<' + uri + '> <' + str(term) + '> "' + str(terms[term]) + '" . '
    for term in rterms:
        for t in rterms[term]:
            update += '<' + uri + '> <' + str(term) + '> "' + str(t)+ '" . '
    update += ' }'

    #TODO: what happens on failure? If delete succeeds and insert fails? Does DELETE/INSERT fix this.
    urllib2.urlopen(endpoint, data='update='+delete)
    urllib2.urlopen(endpoint, data='update='+update)

    return True


class ResourceForm(Form):
    firstName = CharField(required=False)
    lastName = CharField(required=False)
    name = CharField()


class VariantForm(Form):
    variant = CharField(required=False)
    isHidden = BooleanField(required=False)


class BaseVariantFormSet(BaseFormSet):
    def add_fields(self, form, index):
        super(BaseVariantFormSet, self).add_fields(form, index)
        form.fields["variant"] = CharField()

#class MadsForm(Form):
#    authoritativeFullName = CharField(required=True)
#    authoritativeDateName = CharField(required=True)

#class MadsVariantForm(Form):
#    variant = CharField(required=False)
#    isHidden = BooleanField(required=False)

#class BaseMadsVariantFormSet(BaseFormSet):
#    def add_fields(self, form, index):
#        super(BaseVariantFormSet, self).add_fields(form, index)
#        form.fields["variant"] = CharField()

