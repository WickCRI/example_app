from flask import Flask, render_template, request, redirect, url_for, g
from flask_mail import Mail, Message
import sqlite3


app = Flask(__name__)

app.config['DEBUG'] = True
app.config['TESTING'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
#app.config['DEBUG'] = True
app.config['MAIL_USERNAME'] = 'chad.ivic@gmail.com'
app.config['MAIL_PASSWORD'] = 'PrettyPrinted1'
app.config['MAIL_DEFAULT_SENDER'] = ('Chad from blah', 'chad.ivic@gmail.com')
app.config['MAIL_MAX_EMAILS'] = None
#app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_ASCII_ATTACHMENTS'] = False

mail = Mail(app)




def connect_db():
	sql = sqlite3.connect('/Users/chad.ivic/Documents/edXWebProg2020/ExampleSite/data3.db')
	sql.row_factory = sqlite3.Row
	return sql

def get_db():
	if not hasattr(g, 'slqite3'):
		g.sqlite_db = connect_db()
	return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()

@app.route('/')
def index():
	msg = Message('Hey there', recipients=['chad.ivic@scc.tas.edu.au','dominique88@litermssb.com'])
	msg.add_recipient('bajed96184@ermailo.com')
	msg.body = 'This is a test email from Chad\'s app. You don\'t have to reply. Thanks ;)'
	with app.open_resource('surfboard.jpeg') as surfboard:
		msg.attach('surboard.jpeg', 'image/jpeg', surfboard.read())
	mail.send(msg)
	return 'Message has been sent on Wednesday!!!'

@app.route('/bulk')
def bulk():
	users = [{'name' : 'Chad', 'email' : 'chad.ivic@scc.tas.edu.au'}, {'name' : 'Ev', 'email' : 'evkuilenburg@hotmail.com'}]
	with mail.connect() as conn:
		for user in users:
			msg = Message('Bulk!', recipients=[user['email']])
			msg.body = 'Test another email body this afternoon'
			conn.send(msg)
	return 'Bulk worked!!'


@app.route("/homePage")
def homePage():
    db = get_db()
    cur = db.execute('select id, name, message from user')
    results = cur.fetchall()
    return render_template("homePage.html", results=results)

@app.route("/hobbiesPage")
def hobbiesPage():
    return render_template("hobbiesPage.html")

@app.route("/workPage")
def workPage():
    return render_template("workPage.html")

@app.route('/theform', methods=['GET', 'POST'])
def theform():
    if request.method == 'GET':
        return render_template('formForPosts.html')
    else:
        name = request.form['name']
        message = request.form['message']

        db = get_db()
        db.execute('insert into user (name, message) values (?, ?)', [name, message])
        db.commit()
        return redirect(url_for('homePage', name=name, message=message))

@app.route('/viewresults')
def viewresults():
	db = get_db()
	cur = db.execute('select id, name, message from user')
	results = cur.fetchall()

	return f'<h1>The ID is {results[1]["id"]}. The name is {results[1]["name"]}. The blah is {results[1]["message"]}.</h1>'
