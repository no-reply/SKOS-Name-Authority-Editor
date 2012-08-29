{% extends "base.tpl" %}

{% block title %}{{ uri }}{% endblock%}

{% block scripts %}
    <script type="text/javascript"
	    src="http://ajax.googleapis.com/ajax/libs/jquery/1.5.0/jquery.min.js">
    </script>
    <script type="text/javascript"
	    src="../static/jquery.formset.min.js">
    </script>
    <script type="text/javascript">
      $(function() {
	  $('.variant').formset({addText:'Add Variant', deleteText:'Delete'});
	})
      $(function() {
	  $('#savedFlag').delay(1300).fadeOut(500);
	})
      $("button").click(function() {
        $("div#descFull").slideUp(300);
      });
    </script>
{% endblock%}

{% block content %}
    {% if saved %}
    <div id="savedFlag"><p>Saved!</p></div>
    {% endif %}
    <h2><a href="{{ uri }}">{{ short }}</a></h2>
    <form method="post" action="/{{ short }}" id="resourceForm">
      <div>
	<label for="id_name">Full Name:</label>
	{{form.name}}
      </div>
      <div>
	<label for="id_firstname">Given Name:</label>
	{{form.firstName}}
	<label for="id_lastname">Family Name:</label>
	{{form.lastName}}
      </div>
      <div>
	{% for var in variants.forms %}
	<div class="variant">
	  <label>Variant Name:</label>
	  {{ var.variant }}
	  <label>Hidden?</label>
	  {{ var.isHidden }}
	</div>
	{% endfor %}
	{{ variants.management_form }}
      </div>
      <div>
	<input type="submit" value="Save" />
	<a href='/{{short}}'>cancel</a>
      </div>
    </form>
    {% if res %}
    <button id="descToggle">Full Description</button>
    <table class="listing">
      {% for field, values in res.items %}
      {% for value in values %}
      <tr class='{% cycle "odd" "even" %}'>
	<td>{{ field }}</td>
	<td>{{ value.value }}</td>
      </tr>
      {% endfor %}
      {% endfor %}
    </table>

    {% endif %}
{% endblock%}
