from flask import Flask, render_template, request
app = Flask(__name__)

users = {"admin" : "James Bond",
	"user" : "Agent Smith"}

@app.route("/")
def hello():
	return "Hello World!"

@app.route("/user")
def show_user_overview():
	users_str = "<br>".join(users.values())
	return "<h1>Users:</h1><br>{}".format(users_str)

@app.route('/user/<username>')
def show_user_profile(username):
	return 'User {}'.format(username)

@app.route('/pots/')
@app.route('/post/<name>')
def post(name=None):
	return render_template('post.html', name=name)

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/handle_login', methods=['POST'])
def handle_login():
	assert request.method == 'POST'

	username = request.form['username']
	password = request.form['password']

	if username == 'admin' and password == 'admin':
		return 'You have accesed the main server of Zion'
	else:
		error = 'Invalid credentials'
		return render_template("login.html", error=error)

if __name__ == "__main__":
	app.run()
 
