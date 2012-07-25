from django.http import HttpResponse
from django.conf import settings
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import URIRef
from rdflib import Namespace
from rdflib import Literal
import urllib2

class QueryManager:

    def __init__(self, endpoint=settings.ENDPOINT, updateEndpoint=settings.UPDATE, graph=settings.GRAPH, format=JSON):
        self.endpoint = SPARQLWrapper(endpoint)
        self.endpoint.setReturnFormat(format)
        # not using SPARQLwrapper because update endpoints don't seem to work
        self.updateEndpoint = updateEndpoint
        self.graph = graph

    def query(self, query):
        self.endpoint.setQuery(query)
        return self.endpoint.query().convert()
        
    def update(self, query):
        # not using SPARQLwrapper because update endpoints don't seem to work
        response = urllib2.urlopen(self.updateEndpoint, data='update='+query).read()
        if 'error' in response:
            return False
        else:
            return True
        
    def ask(self, uri):
        q = "ASK { GRAPH <" + self.graph + "> { <" + uri + "> ?p ?o . } }"
        return self.query(q)

    def describe(self, uri):
        if self.ask(uri):
            q = "DESCRIBE <" + uri + "> FROM <" + self.graph + ">"
            return self.query(q)[str(uri)]
        else:
            return False
