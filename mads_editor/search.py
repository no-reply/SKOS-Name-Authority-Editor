import django
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.conf import settings
from SPARQLWrapper import SPARQLWrapper, JSON, N3
from query import QueryManager
from rdflib import URIRef
from rdflib import Namespace
from rdflib import Literal

#from http import get_document_url

def search(request, ref=None):
    search_form = SearchForm()
    output = ''
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            
            endpoint = SPARQLWrapper(settings.ENDPOINT)
            endpoint.setReturnFormat(JSON)
            query = 'SELECT ?person ?name WHERE { ?person <http://xmlns.com/foaf/0.1/lastname> "%s" .} LIMIT 100' % form.cleaned_data['searchText']
            endpoint.setQuery(query)
            r = endpoint.query().convert()

            output = output + '<table>\n'
            output = output + str(r['results'])
      #      for person in r['results']['bindings']:
      #          output = output + "<tr>\n<td>" + person['person']['value'] + '</td><td>' + person['name']['value'] + "</td>\n</tr>\n"

            output = output + '</table>'
    return render_to_response("search.tpl", {'form':search_form, 'table': output})

class SearchForm(django.forms.Form):
    searchText = django.forms.CharField()
