<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="{{lang}}" lang="{{lang}}">
  <head>
    <title>{{ short }}</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
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
    </script>
  </head>
  <body>
    <h2><a href="{{ uri }}">{{ short }}</a></h2>
    <table>
      {% for field, value in res.items %}
        <tr>
	  <td>{{ field }}</td>
	  <td>{{ value.0.value }}</td>
	</tr>
      {% endfor %}
    </table>

    <form action="/" method="post" > {% csrf_token %}
      {{form.as_p}}
    </form>
    <form method="post" action="/" id="variantsForm">
      <table>
	<tbody>
	  {% for var in variants.forms %}
	  <tr class="variant">
            <td>{{ var.variant }}</td>
	  </tr>
	  {% endfor %}
	</table>
	{{ variants.management_form }}
    </form>
  </body>
</html>
