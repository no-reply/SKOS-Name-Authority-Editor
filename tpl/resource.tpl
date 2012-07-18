<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="{{lang}}" lang="{{lang}}">
  <head>
    <title>{{ short }}</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
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
  </body>
</html>
