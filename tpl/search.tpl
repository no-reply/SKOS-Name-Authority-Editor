{% extends "base.tpl" %}

{% block title %}Authority Search{% endblock%}

{% block content %}
    <form action="/" method="post" id="searchBox"> {% csrf_token %}
      <label for="id_searchText">Search by name:</label>
      {{form.searchText}}
    </form>
    <div id="searchResults">
      {% if hits.items %}
      <table id="prefNames" class="listing">
	<thead><tr><td><strong>Name Element Matches</strong></td></tr></thead>
	{% for hit, desc in hits.items %}
        <tr class='{% cycle "odd" "even" %}'>
	  <td><a href="/{{ hit }}"> {{ hit }}</a></td>
	  <td>{{ desc }}</td>
	</tr>
	{% endfor %}
      </table>
      {% endif %}
      {% if rhits.items %}
      <table id="varNames" class="listing">
	<thead><tr><td><strong>Partial Matches</strong></td></tr></thead>
	{% for hit, desc in rhits.items %}
          <tr class='{% cycle "odd" "even" %}'>
	    <td><a href="/{{ hit }}">{{ hit }}</a></td>
	    <td>{{ desc }}</td>
	  </tr>
	{% endfor %}
      </table>
      {% endif %}
{% endblock %}
