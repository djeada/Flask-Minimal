#  Flask-Minimal

This is a template for a minimal Flask app. It includes Dockerfile, Makefile, pyproject.toml and set of dependencies defined in requirements.txt.

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
