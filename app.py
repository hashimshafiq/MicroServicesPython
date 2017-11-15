from flask import Flask
from flask import jsonify
from flask import make_response
import json
import sqlite3


path = "D:/OpenSource/MicroServicesPython/micro.db"
app = Flask(__name__)

@app.route("/api/v1/info")
def home_index():

	conn = sqlite3.connect(path)
	print("Database opened")
	api_list = []
	cursor = conn.execute("SELECT buildtime, version,methods, links from apirelease")

	for row  in cursor:
		a_dict = {}
		a_dict['version'] = row[1]
		print(row)
		a_dict['buildtime'] = row[0]
		a_dict['methods'] = row[2]
		a_dict['links'] = row[3]
		api_list.append(a_dict)

	conn.close()
	return jsonify({'api_version':api_list}),200

@app.route("/api/v1/users",methods=["GET"])
def get_users():
	return list_users()

def list_users():
	conn = sqlite3.connect(path)
	api_list = []
	cursor = conn.execute("SELECT username,emailid,password,full_name,id from users")
	print(cursor.rowcount)
	for row in cursor:
		a_dict = {}
		a_dict['username'] = row[0]
		a_dict['emailid'] = row[1]
		a_dict['password'] = row[2]
		a_dict['full_name'] = row[3]
		a_dict['id'] = row[4]
		api_list.append(a_dict)
	conn.close()
	return jsonify({'user_list':api_list}),200



@app.route("/api/v1/users/<int:user_id>" ,methods=['GET'])
def get_users_details(user_id):
	return list_users_details(user_id)

def list_users_details(user_id):
	conn = sqlite3.connect(path)
	api_list = []
	cursor = conn.cursor()
	cursor.execute("SELECT * from users where id=?",(user_id,))
	data = cursor.fetchall()
	if (len(data)!=0):
		user = {}
		user['username'] = data[0][0]
		user['emailid'] = data[0][1]
		user['password'] = data[0][2]
		user['ful_name'] = data[0][3]
		user['id'] = data[0][4]
		api_list.append(user)
	conn.close()
	return jsonify({'user_detail':api_list}),200

@app.errorhandler(404)
def resource_not_found(error):
	return make_response(jsonify({'error':"Resource Not Found!"}),404)


if __name__ == "__main__":
	app.run(host='localhost', port=5000 , debug=True)