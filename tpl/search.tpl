<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="{{lang}}" lang="{{lang}}">
  <head>
    <title>MADS Search</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  </head>
  <body>
    <form action="/" method="post"> {% csrf_token %}
      {{form.as_p}}
    </form>
    <table>
      {% for hit, desc in hits.items %}
        <tr>
	  <td><a href="/{{ hit }}"> {{ hit }}</a></td>
	  <td>{{ desc }}</td>
	</tr>
      {% endfor %}
    </table>
    <table>
      {% for hit, desc in rhits.items %}
        <tr>
	  <td><a href="/{{ hit }}">{{ hit }}</a></td>
	  <td>{{ desc }}</td>
	</tr>
      {% endfor %}
    </table>
  </body>
</html>
