from flask import Flask, request, jsonify
import mysql.connector as ms
from os import getenv
from random import randint
from twilio.rest import Client
from dotenv import load_dotenv
from datetime import datetime
from flask_cors import CORS

load_dotenv()

server = Flask(__name__)
CORS(server)
server.debug = True
mysql_password = getenv('MYSQL_PASSWORD')
twilio_account_sid = getenv('TWILIO_ACCOUNT_SID')
twilio_auth_token = getenv('TWILIO_AUTH_TOKEN')
twilio_phone_No = getenv('TWILIO_PHONE_NO')

client = Client(twilio_account_sid, twilio_auth_token)

otpAndPhoneNo = []

db = ms.connect(
	host = "localhost",
	user = "root",
	password = mysql_password,
	database = "HMS",
	ssl_disabled = True
)

cursor = db.cursor()

def genreate_id(table):
	is_unique = True

	cursor.execute(f"SELECT * FROM {table};")
	login_details = cursor.fetchall()
	id = randint(1000, 9999)

	for i in login_details:
		if id == i[0]:
			is_unique = False

	if is_unique :
		return id
	else:
		genreate_id(table)

def send_otp(phone_no):
	global otpAndPhoneNo

	otp = randint(100000, 999999)
	client.messages.create(
		to = "+91" + str(phone_no),
		from_ = twilio_phone_No,
		body = f"""
			Dear patient,
			Your OTP for signing up on HMS appointment booking platform is: {otp}
			Please enter this OTP within 5 minutes to complete your registration.\n
			If you didn't request this OTP, please ignore this message.
		"""
	)

	otpAndPhoneNo.append([otp, phone_no, datetime.now()])

@server.route('/')
def home():
	return "Welcome to HMS!"

@server.route('/login', methods=['POST'])
def login():
	data = dict(request.get_json())

	try: 
		if data['role'] == 'doctor' :
			cursor.execute(f"SELECT * FROM doctors_login;")
			login_details = cursor.fetchall()
			for i in login_details:
				if data['username'] == i[1]:
					if data['password'] == i[2]:
						return jsonify({"loginSuccess" : "True", "id" : i[0]})
					else:
						return jsonify({"loginSuccess" : "False"}), 404
			return jsonify({"loginSuccess" : "False"})
		elif data['role'] == 'patient':
			cursor.execute(f"SELECT * FROM patient_login;")
			login_details = cursor.fetchall()
			for i in login_details:
				if data['username'] == i[1]:
					if data['password'] == i[2]:
						return jsonify({"loginSuccess" : "True", "id" : i[0]})
					else:
						return jsonify({"loginSuccess" : "False"})
			return jsonify({"loginSuccess" : "False"})
		elif data["role"] == 'receptionist' or data["role"] == "admin":
			cursor.execute(f"SELECT * FROM emp_login;")
			login_details = cursor.fetchall()
			for i in login_details:
				if data['username'] == i[0]:
					if data['password'] == i[1]:
						return jsonify({"loginSuccess" : "True", "authority" : i[2]})
					else:
						return jsonify({"loginSuccess" : "False"})
			return jsonify({"loginSuccess" : "False"})
		else :
			return jsonify({"error" : "Bad request!"}), 400
	except:
		return jsonify({"error" : "Bad request!"}), 400


@server.route('/signup', methods = ['POST'])
def signup():
	data = dict(request.get_json())
	try:
		phone_no = data["phoneNo"]
		send_otp(phone_no)

		return jsonify({ "status" : "all right" }), 200
	except:
		return jsonify({"error" : "Bad request!"}), 400

@server.route('/signup/otp', methods=['POST'])
def recive_otp():
	global otpAndPhoneNo

	did_find = False

	data = dict(request.get_json())

	print(data)

	try :
		recived_otp = int(data['otp'])
		recived_phone_no = data['phoneNo']

		for i in otpAndPhoneNo:
			print((datetime.now() - i[2]).total_seconds())
			if (datetime.now() - i[2]).total_seconds() >= 300:
				otpAndPhoneNo.remove(i)

		for _ in otpAndPhoneNo:
			if recived_phone_no == _[1] :
				did_find = True
				if recived_otp == _[0]:
					return jsonify({ "status" : "sucessfully!" }), 200
				else :
					return jsonify({ "status" : "wrong otp!" }), 200
		if did_find == False :
			return jsonify({ "status" : "time out!" }), 200
	except:
		return jsonify({"error" : "Bad request!"}), 400

@server.route('/signup/details', methods=['POST'])
def signup_details():
	did_exit = False
	keys = ['id', 'name', 'gender', 'dob', 'phoneNo', 'address', 'email']

	data = dict(request.get_json())
	print(data)
	try: 
		username = str(data['username'])
		password = str(data['password'])
		phoneNo = int(data['phoneNo'])

		cursor.execute(f"SELECT * FROM patient_login;")
		login_details = cursor.fetchall()

		for i in login_details:
			if username == i[1]:
				return jsonify({"error" : "Username allready exits!"}), 409

		cursor.execute(f"SELECT * FROM patient_personal_details;")
		login_details = cursor.fetchall()

		for i in login_details:
			if phoneNo == i[4]:
				did_exit = True
				id = int(i[0])
				cursor.execute(f"INSERT INTO patient_login VALUES ({id}, '{username}', '{password}');")
				db.commit()
				return jsonify(dict(zip(keys, i))), 200
			
		if did_exit == False:
			id = genreate_id('patient_personal_details')
			cursor.execute(f"INSERT INTO patient_login VALUES ({id}, '{username}', '{password}');")
			db.commit()
			cursor.execute(f"INSERT INTO patient_personal_details VALUES ({id}, '', '', NULL, 0, '', '');")
			db.commit()
			cursor.execute(f"SELECT * FROM patient_personal_details WHERE id = {id};")
			login_details = cursor.fetchone()
			return jsonify(dict(zip(keys, login_details))), 200
	except:
		return jsonify({"error" : "Bad request!"}), 400

@server.route('/patient/add', methods=['POST'])
def add_patient():
	data = dict(request.get_json())
	print(data)

	try:
		id = int(data['id'])
		name = str(data['name'])
		gender = str(data['gender'])
		dob = data['dob']
		phoneNo = int(data['phoneNo'])
		address = str(data['address'])
		email = str(data['email'])

		cursor.execute(f"UPDATE patient_personal_details SET name='{name}', gender='{gender}', dob='{dob}', phoneNo={phoneNo}, address='{address}', email='{email}' WHERE id={id}")
		db.commit()
		return jsonify({ "status" : "sucessful!" }), 200
	except:
		return jsonify({"error" : "Bad request!"}), 400

@server.route('/addnewid', methods=['GET'])
def newID():
	id = genreate_id('patient_personal_details')
	cursor.execute(f"INSERT INTO patient_personal_details VALUES ({id}, '', '', NULL, 0, '', '');")
	db.commit()
	return jsonify({"id" : id}), 200

@server.route('/patient/delete', methods=['POST'])
def delete_patient():
	try:
		id = dict(request.get_json())['id']
		cursor.execute(f"DELETE FROM patient_personal_details WHERE id={id}")
		db.commit()
		cursor.execute(f"DELETE FROM patient_login WHERE id={id}")
		db.commit()
		return jsonify({ "status" : "sucessful!" }), 200
	except:
		return jsonify({"error" : "Bad request!"}), 400

@server.route('/patient/veiw/personal', methods=['POST'])
def viewPersonalDetails():
	data = dict(request.get_json())
	keys = ['id', 'name', 'gender', 'dob', 'phoneNo', 'address', 'email']

	try: 
		id = data['id']
		try:
			cursor.execute(f"SELECT * FROM patient_personal_details WHERE id = {id};")
			fetched_data = cursor.fetchone()
			return jsonify(dict(zip(keys, fetched_data))), 200
		except:
			return jsonify({"error" : "Data not found for given id!"}), 404
	except:
		return jsonify({"error" : "Bad request!"}), 400

@server.route('/patient/veiw/medication', methods=['GET'])
def viewMedDetails():
	data = dict(request.get_json())
	keys = ['id', 'date', 'medication', 'advise', 'symptoms']

	try: 
		id = data['id']
		try:
			cursor.execute(f"SELECT * FROM patient_med_details WHERE id = {id};")
			fetched_data = cursor.fetchall()
			return jsonify([dict(zip(keys, i)) for i in fetched_data]), 200
		except:
			return jsonify({"error" : "Data not found for given id!"}), 404
	except:
		return jsonify({"error" : "Bad request!"}), 400

@server.route('/patient/update/login_details', methods=['POST'])
def update_patient_login_details():
	data = dict(request.get_json())

	try:
		username = str(data['username'])
		password = str(data['password'])
		id = data['id']
		try:
			cursor.execute(f"UPDATE patient_login SET username = '{username}', password='{password}' WHERE id = {id};")
			db.commit()
		except:
			return jsonify({"error" : "Data not found with given id!"}), 404
	except:
		return jsonify({"error" : "Bad request!"}), 400

@server.route('/patient/appiontment/book', methods=['POST'])
def bookappointment():
	data = dict(request.get_json())

	id = genreate_id('appointment')

	try :
		date = data['date']
		time_slot = data['time_slot']
		pat_id = int(data['pat_id'])
		doc_id = int(data['doc_id'])

		cursor.execute(f"INSERT INTO appointment VALUES ({id}, '{date}', '{time_slot}', {pat_id}, {doc_id});")
		db.commit()

		return jsonify({"id" : id}), 200
	except :
		return jsonify({"error" : "Bad request!"}), 400

@server.route('/patient/appiontment/cancel', methods=['DELETE'])
def deleteAppiontment():
	data = dict(request.get_json())

	try : 
		id = data['app_id']

		cursor.execute(f"DELETE FROM appointment WHERE username={id};")
		db.commit()

		return jsonify({"app_id" : id}), 200
	except:
		return jsonify({"error" : "Bad request!"}), 400


@server.route('/patient/view/availableslots', methods=['POST'])
def veiwslots():
	data = dict(request.get_json())
	keys = ['app_id', 'date', 'time_slot', 'pat_id', 'doc_id']

	try:
		date = data['date']
		doc_id = data['doc_id']
		try:
			cursor.execute(f"SELECT * FROM appointment WHERE date = '{date}' AND doc_id = {doc_id}")
			fetched_data = cursor.fetchone()
			return jsonify(dict(zip(keys, fetched_data))), 200
		except:
			return jsonify({"error" : "Data not found for given doctor id!"}), 404
	except:
		return jsonify({"error" : "Bad request!"}), 400
	
@server.route('/patient/view/appointment/history', methods=['POST'])
def veiwAppointmentHistory():
	data = dict(request.get_json())
	keys = ['app_id', 'date', 'time_slot', 'pat_id', 'doc_id']

	try:
		id = data['pat_id']
		try:
			cursor.execute(f"SELECT * FROM appointment WHERE pat_id = {id};")
			fetched_data = cursor.fetchall()
			return jsonify(dict(zip(keys, fetched_data))), 200
		except:
			return jsonify({"error" : "Data not found for given id!"}), 404
	except:
		return jsonify({"error" : "Bad request!"}), 400

@server.route('/doctor/view/appointments', methods=['GET'])
def veiwAppointments():
	data = dict(request.get_json())
	keys = ['app_id', 'date', 'time_slot', 'pat_id', 'doc_id']

	try:
		date = data['date']
		id = data['doc_id']
		try:
			cursor.execute(f"SELECT * FROM appointment WHERE date = '{date}' AND doc_id = {id};")
			fetched_data = cursor.fetchone()
			return jsonify(dict(zip(keys, fetched_data))), 200
		except:
			return jsonify({"error" : "Data not found for given date!"}), 404
	except:
		return jsonify({"error" : "Bad request!"}), 400

@server.route('/doctor/addmedication', methods=['POST'])
def addMedication() :
	data = dict(request.get_json())

	try :
		id = data['id']
		date = data['date']
		medication = data['medication']
		advise = data['advise']
		symptoms = data['symptoms']

		cursor.execute(f"INSERT INTO patient_med_details VALUES ({id}, '{date}', '{medication}', '{advise}', '{symptoms}');")
		db.commit()

		return jsonify({ "status" : "successful!" }), 200
	except :
		return jsonify({"error" : "Bad request!"}), 400

@server.route('/doctor/all', methods=['GET'])
def fetchAllDoctors():
	keys = ['id', 'name', 'gender', 'dob', 'phoneNo', 'address', 'email', 'doj', 'qualification']

	try :
		cursor.execute("SELECT * FROM doctors;")
		fetched_data = cursor.fetchall()
		return jsonify([dict(zip(keys, i)) for i in fetched_data]), 200
	except :
		return jsonify({"error" : "Bad request!"}), 400
	
@server.route('/employees/all', methods=['GET'])
def fetchAllEmployess():
	keys = ['id', 'name', 'gender', 'dob', 'phoneNo', 'address', 'email', 'doj', 'qualification', 'designation']

	try :
		cursor.execute("SELECT * FROM employees;")
		fetched_data = cursor.fetchall()
		return jsonify([dict(zip(keys, i)) for i in fetched_data]), 200
	except :
		return jsonify({"error" : "Bad request!"}), 400

@server.route('/admin/doctor/add_login', methods=['POST'])
def adminDoctorAdd_login():
	data = dict(request.get_json())

	try :

		username = data['username']
		password = data['password']

		id = genreate_id('doctors_login')

		cursor.execute(f"SELECT * FROM doctors_login;")
		login_details = cursor.fetchall()

		for i in login_details:
			if username == i[1]:
				return jsonify({"error" : "Username allready exits!"}), 409

		cursor.execute(f"INSERT INTO doctors_login VALUES ({id}, '{username}', '{password}');")
		db.commit()
		
		return jsonify({"id" : id}), 200

	except :
		return jsonify({"error" : "Bad request!"}), 400

@server.route('/admin/doctor/add_details', methods=['POST'])
def adminDoctorAdd_details():
	data = dict(request.get_json())

	try :
		id = int(data['id'])
		name = data['name']
		gender = data['gender']
		dob = data['dob']
		phoneNo = int(data['phoneno'])
		address = data['address']
		email = data['email']
		doj = data['doj']
		qualification = data['qualification']
		
		cursor.execute(f"INSERT INTO doctors VALUES ({id}, '{name}', '{gender}', '{dob}', {phoneNo}, '{address}', '{email}', '{doj}', '{qualification}');")
		db.commit()

		return jsonify({ "status" : "successful!" }), 200
	except :
		return jsonify({"error" : "Bad request!"}), 400
	
@server.route('/admin/doctor/update_details', methods=['POST'])
def adminDoctorUpdate_details():
	data = dict(request.get_json())

	try :
		id = int(data['id'])
		name = data['name']
		gender = data['gender']
		dob = data['dob']
		phoneNo = int(data['phoneno'])
		address = data['address']
		email = data['email']
		doj = data['doj']
		qualification = data['qualification']
		
		cursor.execute(f"UPDATE doctors SET name='{name}', gender='{gender}', dob='{dob}', phoneNo={phoneNo}, address='{address}', email='{email}', doj='{doj}', qualification='{qualification}' WHERE doc_id = {id}")
		db.commit()

		return jsonify({ "status" : "successful!" }), 200
	except :
		return jsonify({"error" : "Bad request!"}), 400

@server.route('/admin/doctor/delete', methods=['DELETE'])
def delete_doctor():
	try:
		id = dict(request.get_json())['id']
		cursor.execute(f"DELETE FROM doctors WHERE doc_id={id}")
		db.commit()
		cursor.execute(f"DELETE FROM doctors_login WHERE doc_id={id}")
		db.commit()
		return "sucessful!", 200
	except:
		return jsonify({"error" : "Bad request!"}), 400

@server.route('/admin/employee/add_details', methods=['POST'])
def adminEmployeeAdd_details():
	data = dict(request.get_json())

	try :
		id = genreate_id('employees')
		name = data['name']
		gender = data['gender']
		dob = data['dob']
		phoneNo = int(data['phoneno'])
		address = data['address']
		email = data['email']
		doj = data['doj']
		qualification = data['qualification']
		designation = data['designation']
		
		cursor.execute(f"INSERT INTO employees VALUES ({id}, '{name}', '{gender}', '{dob}', {phoneNo}, '{address}', '{email}', '{doj}', '{qualification}', '{designation}');")
		db.commit()

		return jsonify({ "status" : "successful!" }), 200
	except :
		return jsonify({"error" : "Bad request!"}), 400
	

@server.route('/admin/employee/update_details', methods=['POST'])
def adminEmployeeUpdate_details():
	data = dict(request.get_json())

	try :
		id = int(data['id'])
		name = data['name']
		gender = data['gender']
		dob = data['dob']
		phoneNo = int(data['phoneno'])
		address = data['address']
		email = data['email']
		doj = data['doj']
		qualification = data['qualification']
		designation = data['designation']
		
		cursor.execute(f"UPDATE employees SET name='{name}', gender='{gender}', dob='{dob}', phoneNo={phoneNo}, address='{address}', email='{email}', doj='{doj}', qualification='{qualification}', designation='{designation}' WHERE emp_id = {id}")
		db.commit()

		return jsonify({ "status" : "successful!" }), 200
	except :
		return jsonify({"error" : "Bad request!"}), 400

@server.route('/admin/employee/delete', methods=['DELETE'])
def delete_employee():
	try:
		id = dict(request.get_json())['id']
		cursor.execute(f"DELETE FROM employees WHERE emp_id={id}")
		db.commit()
		return "sucessful!", 200
	except:
		return jsonify({"error" : "Bad request!"}), 400

@server.route('/admin/add_login', methods=['POST'])
def adminAdd_login():
	data = dict(request.get_json())

	try :
		username = data['username']
		password = data['password']

		cursor.execute(f"SELECT * FROM emp_login;")
		login_details = cursor.fetchall()

		for i in login_details:
			if username == i[1]:
				return jsonify({"error" : "Username allready exits!"}), 409

		cursor.execute(f"INSERT INTO emp_login VALUES ('{username}', '{password}', 'R');")
		db.commit()
		
		return jsonify({ "status" : "successful!" }), 200

	except :
		return jsonify({"error" : "Bad request!"}), 400

@server.route('/admin/view/usernames', methods=['GET'])
def adminViewAllusername():

	try :

		cursor.execute(f"SELECT * FROM emp_login;")
		fetched_data = cursor.fetchall()

		return jsonify({ 'usernames' : [i[0] for i in fetched_data ]}), 200
	
	except :
		return jsonify({"error" : "Bad request!"}), 400

@server.route('/admin/login/delete', methods=['DELETE'])
def deleteAdminLogin():
	data = dict(request.get_json())

	try : 
		username = data['username']

		cursor.execute(f"DELETE FROM emp_login WHERE username='{username}';")
		db.commit()

		return jsonify({ "status" : "successful!" }), 200
	except:
		return jsonify({"error" : "Bad request!"}), 400

if __name__ == "__main__":
	server.run()
