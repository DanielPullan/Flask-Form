from flask import Flask, request, render_template, make_response
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
		cur.execute("INSERT INTO checksheet3 (name, location, registration, full_toilet_removed, clean_toilet_cartridge_supplied, new_soap_supplied_to_canteen_and_toilet, new_hand_sanitiser_supplied_to_canteen_and_toilet, toilet_flush_water_refilled, hand_wash_water_refilled_and_dirty_water_emptied, canteen_cleaned, toilet_area_cleaned, toilet_roll_supplied,hand_towels_supplied) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);", (f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13))
		cur.close()

		#return '''<h1>Data Submitted</h1>
		#		  <p>Values: {}{}{}</p>'''.format(name, lastname, email)

		return render_template("checksheet-success.html")

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

			return render_template("form-success.html", name=name, lastname=lastname, email=email)
		except:
			return render_template("form-failure.html")

	return render_template("form-example.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		# get login details from form
		username = request.form['username']
		password = request.form['password']
		pin = request.form['pin']

		# mysql query to check if details exist/are correct
		cur = conn.cursor()
		cur.execute("SELECT * FROM login where username = %s;", (username))
		cur.close()
		results = cur.fetchone()

	#TODO: blah stuff. get the data from the data in blah to become variables and then do the whole if the form password matches the database one, create the cookie and shit

		submittedusername = results[1]
		submittedpassword = results[2]
		submittedpin = results[3]

		if username == submittedusername:
			print("username matches")
		else:
			return "fail"

		if password == submittedpassword:
			print("password matches")
		else:
			return "fail"

		if pin == submittedpin:
			print("pin matches, we good in the hood")
		else: 
			return "fail"

		return result

		# if successful, set the cookie and go to successful login

		# if failed, don't set the cookie, go to sad cat
		#return render_template("form-success.html", name=name, lastname=lastname, email=email)
	return render_template("login.html")
	

@app.route('/set')
def setcookie():
	resp = make_response('Setting cookie!')
	resp.set_cookie('genitals', 'penis')
	return resp

@app.route('/get')
def getcookie():
	framework = request.cookies.get('genitals')
	return framework

if __name__ == "__main__":
	app.run(debug=True)
