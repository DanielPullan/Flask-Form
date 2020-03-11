from flask import Flask, request, render_template, make_response, redirect, url_for
from flask_mail import Message, Mail
import pymysql
from config import where_did_you_come_from, the_greatest_username_ever, the_most_secure_password_ever, emailaddress, emailpassword, test_email_addresses
import datetime
from threading import Thread


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True
## Database stuff

host = where_did_you_come_from
user = the_greatest_username_ever
pw = the_most_secure_password_ever
database = "thing"

conn = pymysql.connect(host=host, port=3306, user=user, passwd=pw, db=database, autocommit=True)

## Email Stuff

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = emailaddress
app.config['MAIL_PASSWORD'] = emailpassword
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

known_issues = ['Database crashes/timesout overnight']


## Global functions

# Send emails. Make sure recipient is in a list.
def sendthething(subject, messagecontent, recipient):
	msg = Message(subject, sender = emailaddress, recipients = recipient)
	msg.body = messagecontent
	mail.send(msg)

def send_mail(subject, recipient, template, **kwargs):
	msg = Message(subject, sender=emailaddress, recipients=[recipient])
	msg.html = render_template(template, **kwargs)
	mail.send(msg)

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
	return render_template("index.html", username=usercookie, userIP=userIP, title=title, known_issues=known_issues)

@app.route('/checksheet', methods=['GET', 'POST']) #allow both GET and POST requests
def checksheet():
	cookie = str(request.cookies.get('OhCanada'))
	if cookie == "GreenAndPleasantLand":
		if request.method == 'POST':
		

			f1 = str(request.form['name'])
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

			return render_template("form-success.html")

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

				# Send emails. Make sure recipient is in a list.
			#def sendthething(subject, messagecontent, recipient):
   			#	msg = Message(subject, sender = emailaddress, recipients = recipient)
   			#	msg.body = messagecontent
   			#	mail.send(msg)

   			#send_mail("New Feedback", app.config['MAIL_DEFAULT_SENDER'], 'mail/feedback.html',
            #     name=name, email=email)


				try:
					addresses = test_email_addresses

					for x in addresses:
						send_mail("New Collection", x , 'mail/email.html', title="Collection", customer=customer_name, collection_point=collection_point, agent=agent_name)
				except Exception as e:
					print(e)
					


				# This currently works. Look into sending an rendered HTML Email
				#sendthething('New transfer', customer_name, ['danjakob@enablebusiness.co.uk'])

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
		cur.execute("select company from collection_point")
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

@app.route('/add-agent', methods=['GET', 'POST']) #allow both GET and POST requests
def add_agent():
	cookie = str(request.cookies.get('OhCanada'))
	if cookie == "GreenAndPleasantLand":
		if request.method == 'POST':
			
			name = request.form['name']
			lastname = request.form['lastname']
			phonenumber =  request.form['phonenumber']
			email = request.form['email']
			business = request.form['business']
			address_line1 = request.form['address_line1']
			address_line2 = request.form['address_line2']
			town = request.form['town']
			county = request.form['county']
			postcode = request.form['postcode']
			siccode = request.form['siccode']


			cur = conn.cursor()
			cur.execute("INSERT INTO agents (name, lastname, phonenumber, email, business, address_line1, address_line2, town, county, postcode, siccode) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);", (name, lastname, phonenumber, email, business, address_line1, address_line2, town, county, postcode, siccode))
			cur.close()

			return render_template("form-success.html")
			
			

		title = "Add Agent"
		return render_template("add-agent.html", title=title)
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
			except Exception as e:
				errormessage = str(e)
				return render_template("form-failure.html", errormessage=errormessage)

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
		return render_template('stare.html', title=title)
	

@app.route('/email-report')
def email_report():
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


		try:
			addresses = test_email_addresses

			for x in addresses:
				send_mail("New Collection", x , 'mail/collection-email-report.html', title=title, transferors_name=transferors_name, transferors_lastname=transferors_lastname, transferors_phonenumber=transferors_phonenumber, transferors_email=transferors_email, transferors_business=transferors_business, transferors_address_line1=transferors_address_line1, transferors_address_line2=transferors_address_line2, transferors_town=transferors_town, transferors_county=transferors_county, transferors_postcode=transferors_postcode, transferors_siccode=transferors_siccode, agent_name=agents_name, agents_lastname=agents_lastname, agents_phonenumber=agents_phonenumber, agents_email=agents_email, agents_business=agents_business, agents_address_line1=agents_address_line1, agents_address_line2=agents_address_line2, agents_town=agents_town, agents_county=agents_county, agents_postcode=agents_postcode, agents_siccode=agents_siccode, collection_name=collection_name, collection_company=collection_company, collection_address_line1=collection_address_line1, collection_address_line2=collection_address_line2, collection_town=collection_town, collection_county=collection_county, collection_postcode=collection_postcode)

			return make_response(redirect('/'))
		

		except Exception as e:
					print(e)
	

		
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





@app.route('/enable-form', methods=['GET', 'POST'])
def enable():
	if request.method == 'POST':
		name = request.form['name']
		location =  request.form['location']
		registration = request.form['registration']
		category = request.form ['category']
		nochange = request.form['nochange']

		#"sole_trader">Sole Trader</option>
        #          	<option value="partnership_1">Partnership (under 50 employees)</option>
        #          	<option value="partnership_2">Partnership (more than 50 employees)</option>
        #          	<option value="government">G

		if category == "sole_trader":
			price = 100
		elif category == "partnership_1":
			price = 200
		elif category == "partnership_2":
			price = 400
		elif category == "government":
			price = 10000
		else:
			print("category not recognised")

		if nochange == "3":
			price = int(price)
			nochange = int(nochange)
			price = (price * nochange)
		else:
			print("something ain't right here.")

		day = int(datetime.datetime.today().weekday())

		price = price * day

		return render_template("enable-success.html", name=name, location=location, registration=registration, category=category, price=price, day=day)
	title = "Enable Form"
	return render_template("enable-form.html", title=title)

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

@app.route('/mail')
def mailandshityo():
	sendthething('Test', 'Email sending seems to be working.', [test_email_addresses[0]])
	return "done"

@app.route('/setup')
## setup some way of preventing this from running.
## potentially a script that deletes self after being ran?
def setup():
	# import os.system
	# form to get database details and first user
	host = request.form['host']
	user = request.form['user']
	password = request.form['password']
	database = request.form['database']

	admin_username = request.form['admin_username']
	admin_password = request.form['admin_password']

	# script to create databases
	#	subprocess.run(['mysql','-u', user, '-p'])
	
	# check connection to database 

	try:
		conn = pymysql.connect(host=host, port=3306, user=user, passwd=pw, db=database, autocommit=True)

	except:
		return "Database setup failed. Contact support."
		# system.play(['video', 'herecomesthemoney.mp4'])

if __name__ == "__main__":
	app.run(debug=true, host='0.0.0.0')
