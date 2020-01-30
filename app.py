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

	userIP = str(request.environ.get('HTTP_X_REAL_IP', request.remote_addr))

	cookie = str(request.cookies.get('OhCanada'))

	if cookie == "GreenAndPleasantLand":
		usercookie = str(request.cookies.get('User'))
		user_logged_in = True
	else:
		usercookie = "Guest"
		user_logged_in = False

	title = "Home"
	return render_template("index.html", username=usercookie, userIP=userIP, title=title)

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

	cur = conn.cursor()
	cur.execute("select name from transferors")
	rows = cur.fetchall()
	cur.close()

	list_of_customers = [str(x) for x, in rows]

	cur = conn.cursor()
	cur.execute("select name from collection_point")
	rows = cur.fetchall()
	cur.close()

	list_of_locations = [str(x) for x, in rows]

	title = "Checksheet"
	return render_template("checksheet.html", list_of_customers=list_of_customers, list_of_locations=list_of_locations, title=title)


@app.route('/waste-transfer', methods=['GET', 'POST'])
def waste_transfer():
	cookie = str(request.cookies.get('OhCanada'))
	if cookie == "GreenAndPleasantLand":
		if request.method == 'POST':
			try:

				customer_name = request.form['customer_name']
				collection_point = request.form['collection_point']
				agent_name = str(request.cookies.get('User'))

				cur = conn.cursor()
				cur.execute("INSERT INTO waste_transfer (customer_name,collection_point,agent_name) VALUES (%s,%s,%s);", (customer_name, collection_point,agent_name))
				cur.close()

				## TODO: Email the waste transfer thing

				res = render_template('form-success.html', result=qwerty)
				return res
			except:
				return render_template('form-success.html')

		cur = conn.cursor()
		cur.execute("select name from transferors")
		rows = cur.fetchall()
		cur.close()

		list_of_customers = [str(x) for x, in rows]

		cur = conn.cursor()
		cur.execute("select name from collection_point")
		rows = cur.fetchall()
		cur.close()

		list_of_locations = [str(x) for x, in rows]

		#list_of_customers = ['Billy', 'Barry', 'Ben', 'Boris']
		#list_of_locations = ['Midgard', 'Isengard', 'Diagon Alley']
		title = "Waste Transfer"
		return render_template("waste-transfer.html", list_of_customers=list_of_customers, list_of_locations=list_of_locations, title=title)
	else:
		res = make_response(redirect('/stare'))
		return res

@app.route('/form-example', methods=['GET', 'POST']) #allow both GET and POST requests
def form_example():
	cookie = str(request.cookies.get('OhCanada'))
	if cookie == "GreenAndPleasantLand":
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

		title = "Form Example"
		return render_template("form-example.html", title=title)
	else:
		res = make_response(redirect('/stare'))
		return res

@app.route('/add-transferor', methods=['GET', 'POST'])
def add_transferor():
	cookie = str(request.cookies.get('OhCanada'))
	if cookie == "GreenAndPleasantLand":
		if request.method == 'POST':
			try:
				name = request.form['name']
				lastname = request.form['lastname']
				phonenumber = request.form['phonenumber']
				email = request.form['email']
				business = request.form['business']
				address_line1 = request.form['address_line1']
				address_line2 = request.form['address_line2']
				town = request.form['town']
				county = request.form['county']
				postcode = request.form['postcode']
				siccode = request.form['siccode']

				cur = conn.cursor()
				cur.execute("INSERT INTO transferors (name,lastname,phonenumber, email, business, address_line1, address_line2, town, county, postcode, siccode) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);", (name, lastname, phonenumber, email, business, address_line1, address_line2, town, county, postcode, siccode))
				cur.close()

				return render_template("form-success.html", name=name, lastname=lastname, email=email)
			except:
				return render_template("form-failure.html")

		title = "Add Transferors"
		return render_template("add-transferor.html", title=title)
	else:
		res = make_response(redirect('/stare'))
		return res


@app.route('/add-location', methods=['GET', 'POST'])
def add_location():
	cookie = str(request.cookies.get('OhCanada'))
	if cookie == "GreenAndPleasantLand":
		if request.method == 'POST':
			try:
				name = request.form['name']
				company = request.form['company']
				address_line1 = request.form['address_line1']
				address_line2 = request.form['address_line2']
				town = request.form['town']
				county = request.form['county']
				postcode = request.form['postcode']

				cur = conn.cursor()
				cur.execute("INSERT INTO collection_point (name,company,address_line1, address_line2, town, county, postcode) VALUES (%s,%s,%s,%s,%s,%s,%s);", (name, company, address_line1, address_line2, town, county, postcode))
				cur.close()

				return render_template("form-success.html")
			except:
				return render_template("form-failure.html")

		title="Add Location"
		return render_template("add-location.html", title=title)
	else:
		res = make_response(redirect('/stare'))
		return res

@app.route('/get-report')
def get_report():
	cookie = str(request.cookies.get('OhCanada'))
	if cookie == "GreenAndPleasantLand":
		current_agent = str(request.cookies.get('User'))

		cur = conn.cursor()
		cur.execute("SELECT * from agents where name = %s", (current_agent))
		agents_result = cur.fetchone()[0:12]
		#number, name, lastname, phonenumber, email, business, address_line1, address_line2, town, county, postcode, siccode = cur.fetchall()
		cur.close()

		# get customer name
		cur = conn.cursor()
		cur.execute("SELECT customer_name FROM waste_transfer where agent_name = %s ORDER BY number DESC LIMIT 1", (current_agent))
		customer = str(cur.fetchone()[0])
		cur.close()

		# get location name
		cur = conn.cursor()
		cur.execute("SELECT collection_point from waste_transfer where agent_name = %s ORDER BY number DESC LIMIT 1", (current_agent))
		job_location = cur.fetchone()[0]
		cur.close()

		# get location details
		cur = conn.cursor()
		cur.execute("SELECT * from collection_point where name = %s", (job_location))
		collection_result = cur.fetchone()[0:8]
		#number, name, lastname, phonenumber, email, business, address_line1, address_line2, town, county, postcode, siccode = cur.fetchall()
		cur.close()

		cur = conn.cursor()
		cur.execute("SELECT * from transferors where name = %s", (customer))
		transferors_result = cur.fetchone()[0:12]
		#number, name, lastname, phonenumber, email, business, address_line1, address_line2, town, county, postcode, siccode = cur.fetchall()
		cur.close()

		collection_name = str(collection_result[1])
		collection_company = str(collection_result[2])
		collection_address_line1 = str(collection_result[3])
		collection_address_line2 = str(collection_result[4])
		collection_town = str(collection_result[5])
		collection_county = str(collection_result[6])
		collection_postcode = str(collection_result[7])

		transferors_name = str(transferors_result[1])
		transferors_lastname = str(transferors_result[2])
		transferors_phonenumber = str(transferors_result[3])
		transferors_email = str(transferors_result[4])
		transferors_business = str(transferors_result[5])
		transferors_address_line1 = str(transferors_result[6])
		transferors_address_line2 = str(transferors_result[7])
		transferors_town = str(transferors_result[8])
		transferors_county = str(transferors_result[9])
		transferors_postcode = str(transferors_result[10])
		transferors_siccode = str(transferors_result[11])

		agents_name = str(agents_result[1])
		agents_lastname = str(agents_result[2])
		agents_phonenumber = str(agents_result[3])
		agents_email = str(agents_result[4])
		agents_business = str(agents_result[5])
		agents_address_line1 = str(agents_result[6])
		agents_address_line2 = str(agents_result[7])
		agents_town = str(agents_result[8])
		agents_county = str(agents_result[9])
		agents_postcode = str(agents_result[10])
		agents_siccode = str(agents_result[11])

		# Note to future Dan. the above works. you need to create a template for a report. Look at the dead trees on the desk for ideas. This was a massive pain to get working right.

		title="Report"
		

		return render_template("report.html", title=title, transferors_name=transferors_name, transferors_lastname=transferors_lastname, transferors_phonenumber=transferors_phonenumber, transferors_email=transferors_email, transferors_business=transferors_business, transferors_address_line1=transferors_address_line1, transferors_address_line2=transferors_address_line2, transferors_town=transferors_town, transferors_county=transferors_county, transferors_postcode=transferors_postcode, transferors_siccode=transferors_siccode, agent_name=agents_name, agents_lastname=agents_lastname, agents_phonenumber=agents_phonenumber, agents_email=agents_email, agents_business=agents_business, agents_address_line1=agents_address_line1, agents_address_line2=agents_address_line2, agents_town=agents_town, agents_county=agents_county, agents_postcode=agents_postcode, agents_siccode=agents_siccode, collection_name=collection_name, collection_company=collection_company, collection_address_line1=collection_address_line1, collection_address_line2=collection_address_line2, collection_town=collection_town, collection_county=collection_county, collection_postcode=collection_postcode)
	else:
		res = make_response(redirect('/stare'))
		return res

@app.route('/print-report')
def print_report():
	cookie = str(request.cookies.get('OhCanada'))
	if cookie == "GreenAndPleasantLand":
		current_agent = str(request.cookies.get('User'))

		cur = conn.cursor()
		cur.execute("SELECT * from agents where name = %s", (current_agent))
		agents_result = cur.fetchone()[0:12]
		#number, name, lastname, phonenumber, email, business, address_line1, address_line2, town, county, postcode, siccode = cur.fetchall()
		cur.close()

		# get customer name
		cur = conn.cursor()
		cur.execute("SELECT customer_name FROM waste_transfer where agent_name = %s ORDER BY number DESC LIMIT 1", (current_agent))
		customer = str(cur.fetchone()[0])
		cur.close()

		# get location name
		cur = conn.cursor()
		cur.execute("SELECT collection_point from waste_transfer where agent_name = %s ORDER BY number DESC LIMIT 1", (current_agent))
		job_location = cur.fetchone()[0]
		cur.close()

		# get location details
		cur = conn.cursor()
		cur.execute("SELECT * from collection_point where name = %s", (job_location))
		collection_result = cur.fetchone()[0:8]
		#number, name, lastname, phonenumber, email, business, address_line1, address_line2, town, county, postcode, siccode = cur.fetchall()
		cur.close()

		cur = conn.cursor()
		cur.execute("SELECT * from transferors where name = %s", (customer))
		transferors_result = cur.fetchone()[0:12]
		#number, name, lastname, phonenumber, email, business, address_line1, address_line2, town, county, postcode, siccode = cur.fetchall()
		cur.close()

		collection_name = str(collection_result[1])
		collection_company = str(collection_result[2])
		collection_address_line1 = str(collection_result[3])
		collection_address_line2 = str(collection_result[4])
		collection_town = str(collection_result[5])
		collection_county = str(collection_result[6])
		collection_postcode = str(collection_result[7])

		transferors_name = str(transferors_result[1])
		transferors_lastname = str(transferors_result[2])
		transferors_phonenumber = str(transferors_result[3])
		transferors_email = str(transferors_result[4])
		transferors_business = str(transferors_result[5])
		transferors_address_line1 = str(transferors_result[6])
		transferors_address_line2 = str(transferors_result[7])
		transferors_town = str(transferors_result[8])
		transferors_county = str(transferors_result[9])
		transferors_postcode = str(transferors_result[10])
		transferors_siccode = str(transferors_result[11])

		agents_name = str(agents_result[1])
		agents_lastname = str(agents_result[2])
		agents_phonenumber = str(agents_result[3])
		agents_email = str(agents_result[4])
		agents_business = str(agents_result[5])
		agents_address_line1 = str(agents_result[6])
		agents_address_line2 = str(agents_result[7])
		agents_town = str(agents_result[8])
		agents_county = str(agents_result[9])
		agents_postcode = str(agents_result[10])
		agents_siccode = str(agents_result[11])

		# Note to future Dan. the above works. you need to create a template for a report. Look at the dead trees on the desk for ideas. This was a massive pain to get working right.

		title="Report"
		

		return render_template("print-report.html", title=title, transferors_name=transferors_name, transferors_lastname=transferors_lastname, transferors_phonenumber=transferors_phonenumber, transferors_email=transferors_email, transferors_business=transferors_business, transferors_address_line1=transferors_address_line1, transferors_address_line2=transferors_address_line2, transferors_town=transferors_town, transferors_county=transferors_county, transferors_postcode=transferors_postcode, transferors_siccode=transferors_siccode, agent_name=agents_name, agents_lastname=agents_lastname, agents_phonenumber=agents_phonenumber, agents_email=agents_email, agents_business=agents_business, agents_address_line1=agents_address_line1, agents_address_line2=agents_address_line2, agents_town=agents_town, agents_county=agents_county, agents_postcode=agents_postcode, agents_siccode=agents_siccode, collection_name=collection_name, collection_company=collection_company, collection_address_line1=collection_address_line1, collection_address_line2=collection_address_line2, collection_town=collection_town, collection_county=collection_county, collection_postcode=collection_postcode)
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
	title = "Login"
	return render_template("login.html", title=title)

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
	title = "Nope"
	return render_template('stare.html', title=title)

@app.route('/humans.txt')
def humans():
	return render_template('humans.txt')


if __name__ == "__main__":
	app.run(debug=True)
