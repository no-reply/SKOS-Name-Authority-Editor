<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="{{lang}}" lang="{{lang}}">
  <head>
    <title>{{ short }}</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <link type="text/css" media="all" href="../static/main.css" />
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
    <style type="text/css">
      html {background-color: #CCC;}
      body {
        font: 13px/1.231 arial,helvetica,clean,sans-serif;
        width: 62em;
        margin: 5em auto;
        padding: 3em 5em;
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
      #prefNames { 
        width: 40em;
        margin: 2em auto;
        background-color: white;
        -moz-box-shadow: 3px 3px 5px 6px #888;
        -webkit-box-shadow: 3px 3px 5px 6px #888;
        box-shadow: 3px 3px 5px 6px #888;
      }
    </style>
  </head>
  <body>
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

    <button id="descToggle">Full Description</button>
    <div id="descFull" style="">
      <table>
	{% for field, value in res.items %}
        <tr>
	  <td>{{ field }}</td>
	  <td>{{ value.0.value }}</td>
	</tr>
	{% endfor %}
      </table>
    </div>

  </body>
</html>
