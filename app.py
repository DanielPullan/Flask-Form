from flask import Flask, request, render_template, make_response, redirect
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
	cookie = str(request.cookies.get('OhCanada'))

	if cookie == "GreenAndPleasantLand":
		usercookie = str(request.cookies.get('User'))
		user_logged_in = True
	else:
		usercookie = "Guest"
		user_logged_in = False


	return render_template("index.html", username=usercookie)

@app.route('/checksheet', methods=['GET', 'POST']) #allow both GET and POST requests
def checksheet():
	cookie = str(request.cookies.get('OhCanada'))
	if cookie == "GreenAndPleasantLand":
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
	else:
		res = make_response(redirect('/stare'))
		return res

	return render_template("checksheet.html")


@app.route('/form-example', methods=['GET', 'POST']) #allow both GET and POST requests
def form_example():
	cookie = str(request.cookies.get('OhCanada'))
	if cookie == "GreenAndPleasantLand":
		print("Poop")
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
	else:
		res = make_response(redirect('/stare'))
		return res

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

		security = 0

		submittedusername = str(results[1])
		submittedpassword = str(results[2])
		submittedpin = str(results[3])

		if submittedusername == username:
			security = security + 1
		else: 
			security = 0

		if submittedpassword == password:
			security = security + 1
		else:
			security = 0
		if submittedpin == pin:
			security = security + 1
		else:
			security = 0

		if security == 3:
			resp = make_response(redirect('/'))
			resp.set_cookie('OhCanada', 'GreenAndPleasantLand')
			resp.set_cookie('User', username)
			return resp
		else:
			print(security)
			print(submittedusername)
			print(submittedpassword)
			print(submittedpin)
			print(username)
			print(password)
			print(pin)
			return "login failed"

	return render_template("login.html")


@app.route('/logout', methods=['GET', 'POST'])
def logout():
	res = make_response(redirect('/'))
	res.set_cookie('OhCanada', 'Quebec')
	return res


@app.route('/get')
def getcookie():
	cookie = str(request.cookies.get('OhCanada'))
	if cookie == "GreenAndPleasantLand":
		return cookie
	else:
		res = make_response(redirect('/stare'))
		res.set_cookie('OhCanada', 'Quebec')
		return res

@app.route('/stare')
def stare():
	return render_template('stare.html')

if __name__ == "__main__":
	app.run(debug=True)
