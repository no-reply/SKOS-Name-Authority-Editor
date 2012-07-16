from django.http import HttpResponse
from django.conf import settings
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import URIRef
from rdflib import Namespace
from rdflib import Literal

class QueryManager:

    def __init__(self, endpoint=settings.ENDPOINT, format=JSON):
        self.endpoint = SPARQLWrapper(endpoint)
        
