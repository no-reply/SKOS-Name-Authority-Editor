from django.shortcuts import render_to_response
from django.conf import settings
from django.forms import Form, CharField
from django.forms.formsets import formset_factory, BaseFormSet
from SPARQLWrapper import SPARQLWrapper, JSON, N3
from query import QueryManager
from rdflib import URIRef
from rdflib import Namespace
from rdflib import Literal

def resource(request, ref=None):
    endpoint = SPARQLWrapper(settings.ENDPOINT)
    endpoint.setReturnFormat(JSON)
    uri = Namespace("http://data.library.oregonstate.edu/person/")[ref]
    query = "ASK { <%s> ?p ?o . }" % uri
    endpoint.setQuery(query)
    test = endpoint.query().convert()
    if test['boolean'] == True:
        query = "DESCRIBE <%s>" % uri
        endpoint.setQuery(query)
        r = endpoint.query().convert()[str(uri)]

        forms = buildForm(r)
    else:
        return "resource not found" #TODO: return a useful error

    return render_to_response("resource.tpl", {'uri': str(uri), 'short': uri.split('/')[-1], 'res': r, 'form': forms['form'], 'variants': forms['variants']})

def buildForm(resource):
    fields = {'name': resource['http://www.w3.org/2004/02/skos/core#label'][0]['value']}
    altLabel = 'http://www.w3.org/2004/02/skos/core#altLabel' 
    initial = []
    if altLabel in resource:
        for variant in resource[altLabel]:
            initial.append({'variant':variant['value']})
        VariantFormSet = formset_factory(VariantForm, extra=0, formset=BaseVariantFormSet)
    else:
        VariantFormSet = formset_factory(VariantForm, extra=1, formset=BaseVariantFormSet)
    variantForm =  VariantFormSet(initial = initial)
    
    form = ResourceForm(fields)
    return {'form':form, 'variants':variantForm}

class ResourceForm(Form):
    name = CharField()

class VariantForm(Form):
    variant = CharField()

class BaseVariantFormSet(BaseFormSet):
    def add_fields(self, form, index):
        super(BaseVariantFormSet, self).add_fields(form, index)
        form.fields["variant"] = CharField()


