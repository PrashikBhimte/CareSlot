from flask import Flask, request, jsonify
import mysql.connector as ms
from os import getenv
from random import randint
from twilio.rest import Client
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

server = Flask(__name__)
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

def genreate_id():
	is_unique = True

	cursor.execute(f"SELECT * FROM patient_personal_details;")
	login_details = cursor.fetchall()
	id = randint(1000, 9999)

	for i in login_details:
		if id == i[0]:
			is_unique = False

	if is_unique :
		return id
	else:
		genreate_id()

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

@server.route('/login', methods=['GET'])
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
						return jsonify({"loginSuccess" : "False"})
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

		return "all right"
	except:
		return jsonify({"error" : "Bad request!"}), 400

@server.route('/signup/otp', methods=['POST'])
def recive_otp():
	global otpAndPhoneNo

	did_find = False

	data = dict(request.get_json())
	try :
		recived_otp = data['otp']
		recived_phone_no = data['phoneNo']

		for i in otpAndPhoneNo:
			print((datetime.now() - i[2]).total_seconds())
			if (datetime.now() - i[2]).total_seconds() >= 300:
				otpAndPhoneNo.remove(i)

		for _ in otpAndPhoneNo:
			if recived_phone_no == _[1] :
				did_find = True
				if recived_otp == _[0]:
					return "sucessfully!"
				else :
					return "wrong otp!"
		if did_find == False :
			return "time out!"
	except:
		return jsonify({"error" : "Bad request!"}), 400

@server.route('/signup/details', methods=['POST'])
def signup_details():
	did_exit = False
	keys = ['id', 'name', 'gender', 'dob', 'phoneNo', 'address', 'email']

	data = dict(request.get_json())
	try: 
		username = str(data['username'])
		password = str(data['password'])
		phoneNo = data['phoneNo']

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
			id = genreate_id()
			cursor.execute(f"INSERT INTO patient_login VALUES ({id}, '{username}', '{password}');")
			db.commit()
			cursor.execute(f"INSERT INTO patient_personal_details VALUES ({id}, '', '', NULL, 0, '', '');")
			db.commit()
			cursor.execute(f"SELECT * FROM patient_personal_details WHERE id = {id};")
			login_details = cursor.fetchone()
			return jsonify(dict(zip(keys, login_details))), 200
	except:
		return jsonify({"error" : "Bad request!"}), 400

@server.route('/addpatient', methods=['POST'])
def add_patient():
	data = dict(request.get_json())

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
		return "sucessful!", 200
	except:
		return jsonify({"error" : "Bad request!"}), 400

@server.route('/addnewid', methods=['GET'])
def newID():
	id = genreate_id()
	cursor.execute(f"INSERT INTO patient_personal_details VALUES ({id}, '', '', NULL, 0, '', '');")
	db.commit()
	return jsonify({"id" : id}), 200

@server.route('/deletepatient', methods=['POST'])
def delete_patient():
	try:
		id = dict(request.get_json())['id']
		cursor.execute(f"DELETE FROM patient_personal_details WHERE id={id}")
		db.commit()
		cursor.execute(f"DELETE FROM patient_login WHERE id={id}")
		db.commit()
		return "sucessful!", 200
	except:
		return jsonify({"error" : "Bad request!"}), 400

if __name__ == "__main__":
	server.run()
