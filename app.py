from flask import Flask, request, render_template #import main Flask class and request object
import pymysql
from config import where_did_you_come_from, the_greatest_username_ever, the_most_secure_password_ever

app = Flask(__name__)

host = where_did_you_come_from
user = the_greatest_username_ever
pw = the_most_secure_password_ever
database = "thing"

conn = pymysql.connect(host=host, port=3306, user=user, passwd=pw, db=database, autocommit=True)

@app.route('/')
def home():
	return render_template("index.html")

@app.route('/form-example', methods=['GET', 'POST']) #allow both GET and POST requests
def form_example():
	if request.method == 'POST':
		try:
			name = request.form['name']
			lastname = request.form['lastname']
			email = request.form['email']

			cur = conn.cursor()
			cur.execute("INSERT INTO users (name,lastname,email) VALUES (%s,%s,%s);", (name, lastname,email))
			cur.close()

			#return '''<h1>Data Submitted</h1>
			#		  <p>Values: {}{}{}</p>'''.format(name, lastname, email)

			return render_template("form-success.html", name=name, lastname=lastname, email=email)
		except:
			return render_template("form-failure.html")

	return render_template("form-example.html")

if __name__ == "__main__":
	app.run(debug=True)
