# Flask-Basic

The Hypertext Transfer Protocol
The Hypertext Transfer Protocol (HTTP) is designed to enable comunication between clients and servers.

Two common methods:
- GET: Requests data from server (ex. typing in google search engine)
- POST: Submits data to be processed by the server (ex. clicking submit button on bank page)

HyperText Markup Language

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
 
 HTML Forms
 
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
 
  ```html
 <form action="http://www.bing.com/search" method="GET">
  Bing search:<br>
  <input type="text" name="q" value="Search">
  <br>
  <input type="submit" value="Submit">
  </form>
  ```
  
  What is Flask?
Flask is a micro web application framework.

You can use Flask to:
- build a static website
- build dynamic websites
- build API server

Features:
- debugger
- unit testing
- open source
- no db abstraction layer, no form validation
 
 FLask Hello World
   ```Python
 from flask import Flask
 app = Flask(__name__)
 
 @app.route("/")
 def hello():
  return "Hello World!"
  
  if __name__ == "__main__":
    app.run()
  ```
  
 Argument for Flask object tells it where to look for templates, static files, and so on. Use __name__ for a single module.
 route() decorator specifies which URL will call that function.
 
 
