<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="{{lang}}" lang="{{lang}}">
  <head>
    <title>MADS Search</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <link type="text/css" media="all" href="http://data.library.oregonstate.edu:8081/static/main.css" />
    <style type="text/css">
      html {background-color: #CCC;}
      body {
        font: 13px/1.231 arial,helvetica,clean,sans-serif;
        width: 62em;
        margin: 5em auto ;
        padding: 3em 5em 10em;
        background-color: #EEE;
        -moz-box-shadow: 3px 3px 5px 6px #888;
        -webkit-box-shadow: 3px 3px 5px 6px #888;
        box-shadow: 3px 3px 5px 6px #888;
      }
      h1 { 
        font-family:arial,helvetica,clean,sans-serif;
        text-align: center;
        margin: .5em;
      }
      #searchBox {
        width: 20em;
        margin: 5em auto 1em;
      }
      #id_searchText {
        width: 20em;
        margin: 0 auto;
      }
      #savedFlag {
        float:right; 
        margin: -3em 3em; 
        width: 8em; 
        height: 3.5em; 
        text-align: center; 

        background-color: #FFC; 
        -webkit-box-shadow: 
          inset 0 0 2px  rgba(0,0,0,0.4),
                0 0 4px rgba(0,0,0,0.4); 
        -moz-box-shadow: 
          inset 0 0 2px  rgba(0,0,0,0.4),
                0 0 4px rgba(0,0,0,0.4); 
        box-shadow: 
            inset 0 0 2px  rgba(0,0,0,0.4),
                  0 0 4px rgba(0,0,0,0.4); 
      }
      input:not([type=submit]) {
        font-weight: bold;
        border: 3px solid white; 
        -webkit-box-shadow: 
          inset 0 0 3px  rgba(0,0,0,0.1),
                0 0 6px rgba(0,0,0,0.1); 
        -moz-box-shadow: 
          inset 0 0 3px  rgba(0,0,0,0.1),
                0 0 6px rgba(0,0,0,0.1); 
        box-shadow: 
            inset 0 0 3px  rgba(0,0,0,0.1),
                  0 0 6px rgba(0,0,0,0.1); 
        padding: 5px;
        background: rgba(255,255,255,0.5);
        margin: 0 3em 8px 10px;
      }
      #prefNames, #varNames { 
        width: 40em;
        margin: 2em auto;
        background-color: #FFF;
        -moz-box-shadow: 1px 1px 4px 4px #CCC;
        -webkit-box-shadow: 1px 1px 4px 4px #CCC;
        box-shadow: 1px 1px 4px 4px #CCC;
      }
    </style>
  </head>
  <body>
    <h1>SKOS/MADS Name Authority Editor</h1>
    <form action="/" method="post" id="searchBox"> {% csrf_token %}
      <label for="id_searchText">Search by name:</label>
      {{form.searchText}}
    </form>
    <div id="searchResults">
      {% if hits.items %}
      <table id="prefNames">
	{% for hit, desc in hits.items %}
        <tr>
	  <td><a href="/{{ hit }}"> {{ hit }}</a></td>
	  <td>{{ desc }}</td>
	</tr>
	{% endfor %}
      </table>
      {% endif %}
      {% if rhits.items %}
      <table id="varNames">
	{% for hit, desc in rhits.items %}
        <tr>
	  <td><a href="/{{ hit }}">{{ hit }}</a></td>
	  <td>{{ desc }}</td>
	</tr>
	{% endfor %}
      </table>
      {% endif %}
  </body>
</html>
