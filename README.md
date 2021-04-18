# Flask-Basic

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
If you want more functionality you must install addons.

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
 
 
 <h2>Make the server available in LAN: </h2>
 
 ```Python
 app.run(host='0.0.0.0')
 ```
 
