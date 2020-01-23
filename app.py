from flask import Flask, request #import main Flask class and request object
import pymysql
import config

app = Flask(__name__) #create the Flask app

host = where_did_you_come_from
user = the_greatest_username_ever
pw = the_most_secure_password_ever
database = all_your_base_are_belong_to_us

conn = pymysql.connect(host=host, port=3306, user=user, passwd=pw, db=database, autocommit=True)


@app.route('/form-example', methods=['GET', 'POST']) #allow both GET and POST requests
def form_example():
	if request.method == 'POST':
		name = request.form['name']
		lastname = request.form['lastname']
		email = request.form['email']

		cur = conn.cursor()
		cur.execute("INSERT INTO users (name,lastname,email) VALUES (%s,%s,%s);", (name, lastname,email))
		cur.close()

		return '''<h1>Data Submitted</h1>
				  <p>Values: {}{}{}</p>'''.format(name, lastname, email)

	return '''<form method="POST">
				  Name: <input type="text" name="name"><br>
				  Lastname: <input type="text" name="lastname"><br>
				  Email: <input type="text" name="email"><br>
				  <input type="submit" value="Submit"><br>
			  </form>'''

if __name__ == "__main__":
	app.run(debug=True)
