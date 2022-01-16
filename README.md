# Flask-Basic

VERY MINIMAL:

 ```Python
from flask import Flask
app = Flask(name)
@app.route("/")
def main():
    return "Hello World"
```  

but we need a bit more to get started on a serious project.

Learn how to make a simple Flask web app.

TABLE OF CONTENTS
1. ABOUT FLASK
2. PROJECT SPECIFIACTION
3. USAGE

<h1>The Hypertext Transfer Protocol</h1>
The Hypertext Transfer Protocol (HTTP) is designed to enable comunication between clients and servers.

Two common methods:
- GET: Requests data from server (ex. typing in google search engine)
- POST: Submits data to be processed by the server (ex. clicking submit button on bank page)

<h1>HyperText Markup Language </h1>

- Used for every website on the internet.
- Your browser knows how to render it.
- Developed by the World Wide Web Consortium.
- Current version HTML5.


A simple HTML document:

```html
<!DOCTYPE html>
<html>
  
  <head>
  <title>Title of your page.</title>
  </head>
  
  <body>
  <p>Hello world!</p>
  </body>
  
 </html>
```
 
<h2> HTML Forms </h2>
 
 ```html
 <form>
  
  <!-- form elements -->
  
  </form>
```  
  
  - text input
  - checkboxes
  - radio buttons
  - submit buttons
 
 <form>

A simple example:
  
 ```html
 First name: <br>
 <input type="text" name="firstname">
 <br>
 Last name:<br>
 <input type="text" name="lastname">
 <br>
 Password:<br>
 <input type="password" name="password">
 </form>
 ```
 
 Another example:

  ```html
 <form action="http://www.bing.com/search" method="GET">
  Bing search:<br>
  <input type="text" name="q" value="Search">
  <br>
  <input type="submit" value="Submit">
  </form>
  ```
  
<h1>What is Flask?</h1>
Flask is a micro web application framework.
Flask is only the foundation for adding functionality.
If you want more functionality you must install addons. <br>

You can use Flask to:
- build a static website
- build dynamic websites
- build API server

Features:
- debugger
- unit testing
- open source
- no db abstraction layer, no form validation
 
 <h2>Flask Hello World</h2>
 
   ```Python
 from flask import Flask
 app = Flask(__name__)
 
 @app.route("/")
 def hello():
  return "Hello World!"
  
  if __name__ == "__main__":
    app.run()
  ```
  
 All flask apps are instances of Flask class.
 The argument for Flask object tells it where to look for templates, static files, and so on. Use __name__ for a single module.
 
The handlers that respond to requests from web browsers or other clients are known as views. Python functions are used to write handlers. Every view function corresponds to one or more request URLs. 
The decorator route() specifies which URL will call that function.
 
<h2>Templates</h2>

Templates allow you to separate the logic of your project from the layout and presentation.

Let's look at an example index.html file:

 ```html
<html> 
  <head> 
    <title>{{ title }} - microblog</title> 
  </head> 
  <body> 
    <h1>Hello, {{ user.username }}!</h1> 
  </body> 
</html>
```

All templates consist of regular html with dynamic parts enclosed with {{…}}.
Variables are passed to the template from Python code.

 ```Python
@app.route(‘/’)
def index(): 
  user = {“name”:”admin”} 
  return render_template(‘index.html’, title=’Title Page’, user=user)
```

Flask uses Jinja2 templating engine.

The fact that Jinja2 supports control statements inside: %...% blocks is what makes it so powerful.

 ```html
<html> 
  <head> 
    {% if title %} 
      <title> {{title}} - microblog </title> 
    {% else %} 
      <title> Welcome! </title> 
    {% endif %}
  </head> 
</html>
```

You can even create simple loops:

 ```html
{% for i in range(11) %}
 {{ i }}
{% endfor %}
```

Last but not least, Jinja2's template inheritance feature allows us to move the page layout components that are shared by all templates and place them in a base template from which all other templates are derived.


<h1>Installation</h1>
 
    $ git clone https://github.com/djeada/Minimal-Flask-App.git
    $ cd Minimal-Flask-App
    $ python3 -m venv env
    $ source env/bin/activate
    $ python3 src/main.py

 <h2>Make the server available on LAN </h2>
 
Modify the code where the <code>run</code> method is called on the Flask instance (here named app): 

 ```Python
 app.run(host='0.0.0.0')
 ```

<h1>Documentation</h1>
The documentation is built with Sphinx.

    cd docs
    sphinx-quickstart
    vim conf.py
    vim index.rst
    sphinx-apidoc -o . ..
    make html
