from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.conf import settings
from django.forms import Form, CharField, BooleanField
from django.forms.formsets import formset_factory, BaseFormSet
from SPARQLWrapper import SPARQLWrapper, JSON, N3
import urllib2
import pynoid
import random
from query import QueryManager
from rdflib import URIRef
from rdflib import Namespace
from rdflib import Literal
from namespaces import Ns

namespaces = Ns.namespaces
ns = namespaces
queryManager = QueryManager()

def resource(request, ref=None):
    saved = False # set saved to false until post is successful
    uri = Namespace("http://data.library.oregonstate.edu/person/")[ref]
    data = ''
    # deal with updates if this is a form submit
    if request.method == 'POST':
        # get data to delete
        resource = queryManager.describe(uri)
        try:
            resource = resource
        except:
            resource = {}
        
        # get form data and put it in a dict
        resForm = ResourceForm(request.POST)
        VariantFormSet = formset_factory(VariantForm)
        varForm = VariantFormSet(request.POST)
        if resForm.is_valid() and varForm.is_valid():
            data = {
                'res': resForm.cleaned_data,
                'var': varForm.cleaned_data
                }
            saved = processForm(uri, data, resource)

    # if the uri exists, try to describe it and build an edit form 
    # retrieving data again if we just processed a form

    resource = queryManager.describe(uri)
    if resource:
        forms = buildForm(resource)
    else:
        #TODO: return a useful error
        return HttpResponse("resource not found", status=404) 

    return render_to_response("resource.tpl", {'uri': str(uri), 'short': uri.split('/')[-1], 'res': resource, 'form': forms['form'], 'variants': forms['variants'], 'saved': saved, 'data': resource})

def new(request, ref=None):
    uriNeeded = True
    while uriNeeded == True:
        # assign an identifier
        identifier = pynoid.mint('zeek', random.randint(0, 100000))
        uri = Namespace("http://data.library.oregonstate.edu/person/")[identifier]
        uriNeeded = queryManager.ask(uri) # if this identifier is already in use, let's get another one
    forms = buildForm()
       
    return render_to_response("resource.tpl", {'uri': str(uri), 'short': uri.split('/')[-1], 'res': {}, 'form': forms['form'], 'variants': forms['variants']})

def confirm(request, ref=None):
    #TODO: add confirmation step to form submit
    pass

def merge(request, uriMerge=None, uriTarget=None):
    uriMerge = Namespace("http://data.library.oregonstate.edu/person/")[uriMerge]
    uriTarget = Namespace("http://data.library.oregonstate.edu/person/")[uriTarget]
    merge = queryManager.describe(uriMerge)
    target = queryManager.describe(uriTarget)

    if request.method == 'POST':
        sameAs = "INSERT DATA {<" + uriMerge + "> owl:sameAs <" + uriTarget + "> .}"
        queryManager.update(sameAs)
        # get form data and put it in a dict
        resForm = ResourceForm(request.POST)
        VariantFormSet = formset_factory(VariantForm)
        varForm = VariantFormSet(request.POST)
        if resForm.is_valid() and varForm.is_valid():
            data = {
                'res': resForm.cleaned_data,
                'var': varForm.cleaned_data
                }
            saved = processForm(uriTarget, data, resource)

    # these labels will be merged into the target as skos:hiddenLabel
    #TODO: exclude duplicate names
    mergeLabels = [str(ns['skos']['prefLabel']), str(ns['skos']['altLabel']), str(ns['skos']['hiddenLabel']), str(ns['foaf']['name'])]
    for field in merge:
        if field in mergeLabels:
            for value in merge[field]:
                if str(ns['skos']['hiddenLabel']) in target:
                    target[str(ns['skos']['hiddenLabel'])].append(value)
                else: 
                    target[str(ns['skos']['hiddenLabel'])] = merge[field]

    #TODO: mark old record for deletion
    # do this with a hidden form?
    
    forms = buildForm(target)
    data = target
    return render_to_response("merge.tpl", {'uriMerge': str(uriMerge), 'uri': str(uriTarget), 'mergeShort': uriMerge.split('/')[-1], 'short': uriTarget.split('/')[-1], 'res': target, 'form': forms['form'], 'variants': forms['variants']})

def buildForm(resource={}):
    fields = {}
    try:
        fields = {'name': resource[str(ns['skos']['prefLabel'])][0]['value']}
    except:
        pass
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

    if (altLabel in resource):
        for variant in resource[altLabel]:
                initial.append({'variant':variant['value'], 'isHidden':False})

    if (hiddenLabel in resource):
        for variant in resource[hiddenLabel]:
            initial.append({'variant':variant['value'], 'isHidden':True})

        VariantFormSet = formset_factory(VariantForm, extra=0, formset=BaseVariantFormSet)
    else:
        VariantFormSet = formset_factory(VariantForm, extra=1, formset=BaseVariantFormSet)
    variantForm =  VariantFormSet(initial = initial)
    
    form = ResourceForm(fields)
    return {'form':form, 'variants':variantForm}


def processForm(uri, data, olddata):
    new = queryManager.ask(uri) # is this a new entry?
    # create a dictionary object of term uris and their form data
    #TODO: is there a good way to move all term matching to a single configurable location?
    terms={
        ns['foaf']['familyName']: data['res']['lastName'],
        ns['foaf']['givenName']: data['res']['firstName'],
        ns['skos']['prefLabel']: data['res']['name'],
        }
    # and another dict for repeatable terms
    rterms={
        ns['skos']['altLabel']: [],
        ns['skos']['hiddenLabel']: [],
        }

    # find all alt and hidden labels
    for label in data['var']:
        try:
            if label['isHidden']:
                rterms[ns['skos']['hiddenLabel']].append(label['variant'])
            else:
                rterms[ns['skos']['altLabel']].append(label['variant'])
        except:
            continue
        
    if new == False:
    #TODO: make delete make sense. This is a huge mess of trial and error.
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

        delStatus = queryManager.update(delete)
    else: 
        delStatus = True

    # Insert Updated data
    update =  '{'
    # loop through dict objects and add a triple for each term
    for term in terms:
        if terms[term]:
            update += '<' + uri + '> <' + str(term) + '> "' + terms[term] + '" . '
    for term in rterms:
        for value in rterms[term]:
            if value:
                update += '<' + uri + '> <' + str(term) + '> "' + str(value)+ '" . '
    if new == True:
        update += '<' + uri + '> <' + ns['rdf']['type']+ '> "' + ns['mads']['RWO'] + '" . '
        update += '<' + uri + '> <' + ns['rdf']['type']+ '> "' + ns['foaf']['person'] + '" . '
    update += ' }'

    #TODO: what happens on failure? If delete succeeds and insert fails? Does DELETE/INSERT fix this.
    upStatus = queryManager.insert(update)

    return delStatus and upStatus


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

