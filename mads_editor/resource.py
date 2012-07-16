from django.http import HttpResponse
from django.conf import settings
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
        output = "<div>" + str(uri) + "</div>\n"
        output = output + '<table>\n'
        for field in r:
            for value in r[field]:
                output = output + "<tr>\n<td>" + field + "</td><td>" + value['value'] + "</td></tr>"
        output = output + '</table>'
    else:
        output = 'ID is missing or malformed.'
    return HttpResponse(output)
