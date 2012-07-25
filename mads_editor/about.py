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

namespaces = Ns.namespaces
ns = namespaces
queryManager = QueryManager()

def about(request, ref=None):
    # get a person count
    query = """SELECT ?person (COUNT(?person) as ?pCount) WHERE { 
        ?person <%(label)s> ?o .
        }""" % {'label': str(ns['skos']['prefLabel']), 'person': str(ns['foaf']['person'])}
    personCount = queryManager.query(query)['results']['bindings'][0]['pCount']['value']
    return HttpResponse(personCount, status=404) 
    
    
