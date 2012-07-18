from django.conf import settings
from django.forms import Form, CharField
from django.shortcuts import render_to_response
from SPARQLWrapper import SPARQLWrapper, JSON, N3
from query import QueryManager
from rdflib import URIRef
from rdflib import Namespace
from rdflib import Literal

#from http import get_document_url

def search(request, ref=None):
    search_form = SearchForm()
    hits = {}
    rhits = {}
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            endpoint = SPARQLWrapper(settings.ENDPOINT)
            endpoint.setReturnFormat(JSON)

            query = """SELECT ?hit, ?regexhit WHERE 
            {{?hit <http://xmlns.com/foaf/0.1/lastname> '%(s)s' .} UNION 
             {?hit <http://xmlns.com/foaf/0.1/firstname> '%(s)s' .} UNION 
             {?hit <http://xmlns.com/foaf/0.1/name> '%(s)s' .} UNION 
             {?regexhit <http://www.w3.org/2004/02/skos/core#label> ?name FILTER regex(?name, '%(s)s', "i")} UNION 
             {?regexhit <http://www.w3.org/2004/02/skos/core#altLabel> ?name FILTER regex(?name, '%(s)s', "i")} UNION 
             {?hit <http://www.w3.org/2004/02/skos/core#label> '%(s)s' .} UNION
             {?hit <http://www.w3.org/2004/02/skos/core#altLabel> '%(s)s' .}} 
             LIMIT 100""" % {'s': form.cleaned_data['searchText']}

            endpoint.setQuery(query)
            r = endpoint.query().convert()
            for person in r['results']['bindings']:
                level = 'hit'
                try:
                    uri = person['hit']['value']
                except:
                    uri = person['regexhit']['value']
                    level = 'regex'
                uristr = str(uri)
                query = 'DESCRIBE <' + uristr + '>'
                endpoint.setQuery(query)
                desc = endpoint.query().convert()
                suri = uristr.split('/')[-1]
                if level == 'hit':
                    hits[suri] = desc[uri][u'http://www.w3.org/2004/02/skos/core#label'][0][u'value']
                elif not suri in hits:
                    rhits[suri] = desc[uri][u'http://www.w3.org/2004/02/skos/core#label'][0][u'value']
            
    return render_to_response("search.tpl", {'form':search_form, 'hits': hits, 'rhits': rhits})

class SearchForm(Form):
    searchText = CharField()
