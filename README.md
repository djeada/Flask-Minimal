# Minimal-Flask-App

This is a template for a minimal Flask app. It includes Dockerfile, Makefile, pyproject.toml and set of dependencies defined in requirements.txt.

## Table of Contents
<!--ts-->

- [Minimal-Flask-App](#Minimal-Flask-App)
- [Problem-description](#Problem-description)
- [Theory](#Theory)
  - [The-Hypertext-Transfer-Protocol](#The-Hypertext-Transfer-Protocol)
  - [HyperText-Markup-Language](#HyperText-Markup-Language)
  - [HTML-Forms](#HTML-Forms)
  - [What-is-Flask?](#What-is-Flask?)
  - [Flask-Hello-World](#Flask-Hello-World)
  - [Templates](#Templates)
- [Installation](#Installation)
  - [Make-the-server-available-on-LAN](#Make-the-server-available-on-LAN)
  - [Start-the-app-in-Docker](#Start-the-app-in-Docker)
- [Documentation](#Documentation)

<!--te-->

# Problem description

When creating a new Flask app, it is often useful to have a template that can be used to start from. 

The bare minmal Flask app consits of only a few lines of code:

 ```Python
from flask import Flask
app = Flask(name)
@app.route("/")
def main():
    return "Hello World"
```  

We usually want a bit more than that. That's why I decided to create this template.

# Theory

## The Hypertext Transfer Protocol
The Hypertext Transfer Protocol (HTTP) is designed to enable comunication between clients and servers.

Two common methods:
- GET: Requests data from server (ex. typing in google search engine)
- POST: Submits data to be processed by the server (ex. clicking submit button on bank page)

## HyperText Markup Language 

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
 
## HTML Forms 
 
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
<br> Last name:<br>
<input type="text" name="lastname">
<br> Password:
<br>
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
  
## What is Flask?
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
 
## Flask Hello World

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
 
## Templates

Templates allow you to separate the logic of your project from the layout and presentation.

Let's look at an example index.html file:

```html
<html>

<head>
    <title>{{ title }} - microblog</title>
</head>

<body>
    # Hello, {{ user.username }}!
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

# Installation

## Set Up for Unix, MacOS

1. Download the code repository from GitHub:
    
```Bash
git clone https://github.com/djeada/Minimal-Flask-App.git
cd Minimal-Flask-App
```

2. Install modules via VENV:

```Bash
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

3. Start the app:

```Bash
python src/app.py
```

To make the server available on the LAN, modify the code where the <code>run</code> method is called on the Flask instance (here named app): 

```Python
app.run(host='0.0.0.0')
```

##  Start the app in Docker

1. Download the code from the repository:
    
```Bash
git clone https://github.com/djeada/Minimal-Flask-App.git
cd Minimal-Flask-App
```

Start the APP in Docker:

```Bash
docker-compose up --build 
```
 
In your browser, go to http://localhost:85. The app should now be working. 

# Documentation

Sphinx is used to generate the documentation from docstrings.

If documentation has not yet been created, use:

    mkdir -p docs && cd docs
    sphinx-quickstart
    sphinx-apidoc -o . ..
    make html
    
To change the configuration, use:

    vim docs/source/conf.py

To alter the contents of a file, for example, <code>docs/soruce/index.rst</code>, use:

    vim docs/source/index.rst

To update the documentation, use:

    make html

To view the documentation, use:

    firefox docs/build/html/index.html 

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
