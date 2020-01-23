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

@app.route('/checksheet', methods=['GET', 'POST']) #allow both GET and POST requests
def checksheet():
	if request.method == 'POST':
		try:
			#name = request.form['name']
			#lastname = request.form['lastname']
			#email = request.form['email']

			f1 = request.form['name']
			f2 = request.form['location']
			f3 = request.form['registration']
			f4 = request.form['full_toilet_removed']
			f5 = request.form['clean_toilet_cartridge_supplied']
			f6 = request.form['new_soap_supplied_to_canteen_and_toilet']
			f7 = request.form['new_hand_sanitiser_supplied_to_canteen_and_toilet']
			f8 = request.form['toilet_flush_water_refilled']
			f9 = request.form['hand_wash_water_refilled_and_dirty_water_emptied']
			f10 = request.form['canteen_cleaned']
			f11 = request.form['toilet_area_cleaned']
			f12 = request.form['toilet_roll_supplied']
			f13 = request.form['hand_towels_supplied']

			cur = conn.cursor()
			cur.execute("INSERT INTO checksheets (f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12, f13) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);", (f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12, f13))
			cur.close()

			#return '''<h1>Data Submitted</h1>
			#		  <p>Values: {}{}{}</p>'''.format(name, lastname, email)

			return render_template("checksheet-success.html")
		except:
			return render_template("checksheet-failure.html")

	return render_template("checksheet.html")


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
