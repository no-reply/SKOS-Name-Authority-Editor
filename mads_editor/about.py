from django.shortcuts import render_to_response
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

namespaces = Ns.namespaces
ns = namespaces

def about(request, ref=None):
    endpoint = SPARQLWrapper(settings.ENDPOINT)
    endpoint.setReturnFormat(JSON)

    # get a person count
    query = "SELECT ?person WHERE { ?person <%(label)s> ?o ; a <%(person)s> }" % {'label': str(ns['skos']['prefLabel'], 'person': str(ns['foaf']['person']){
    endpoint.setQuery(query)
    test = endpoint.query().convert()
