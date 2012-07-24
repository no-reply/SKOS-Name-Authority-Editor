from django.conf import settings
from rdflib import Namespace

class Ns:
    namespaces = {
        'rdf': Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#'),
        'rdfs': Namespace('http://www.w3.org/2000/01/rdf-schema#'),
        'owl': Namespace('http://www.w3.org/2002/07/owl#'),
        'skos': Namespace('http://www.w3.org/2004/02/skos/core#'),
        'foaf': Namespace('http://xmlns.com/foaf/0.1/'),
        'mads': Namespace('http://www.loc.gov/mads/rdf/v1#'),
        'person': Namespace(settings.PERSON_NS),
        'auth': Namespace(settings.MADS_AUTH_NS),
        }
        
