from flask import Flask
from flask import jsonify
from flask import make_response
from flask import abort
from flask import request
import json
from time import strftime
from time import gmtime
import sqlite3


path = "D:/OpenSource/MicroServicesPython/micro.db"
app = Flask(__name__)

@app.route("/api/v2/info")
def home_index2():

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

@app.route("/api/v2/tweets",methods=['GET'])
def get_tweets():
	return list_tweets()


def list_tweets():
	conn = sqlite3.connect(path)
	api_list=[]
	cursor = conn.execute("SELECT username, body, tweet_time, id FROM tweets")
	data = cursor.fetchall()
	if data != 0:
		for row in data:
			tweets = {}
			tweets['Tweet By'] = row[0]
			tweets['Body'] = row[1]
			tweets['Timestamp'] = row[2]
			tweets['id'] = row[3]
			api_list.append(tweets)

	conn.close()
	return jsonify({'tweets_list': api_list}),200

@app.route("/api/v2/tweets",methods=['POST'])
def add_tweets():
	user_tweet = {}
	if not request.json or not 'username' in request.json or not 'body' in request.json:
		abort(400)
	user_tweet['username'] = request.json['username']
	user_tweet['body'] = request.json['body']
	user_tweet['created_at'] = strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())
	print(user_tweet)
	return jsonify({'status':add_tweet(user_tweet)}),201

def add_tweet(new_tweets):
	conn = sqlite3.connect(path)
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM users WHERE username=?",(new_tweets['username'],))
	data = cursor.fetchall()
	if len(data) == 0:
		abort(404)
	else:
		cursor.execute("INSERT into tweets (username,body,tweet_time) VALUES(?,?,?)",(new_tweets['username'],new_tweets['body'],new_tweets['created_at']))
		conn.commit()
	return "success"



@app.route('/api/v2/tweets/<int:id>', methods=['GET'])
def get_tweet(id):
	return list_tweet(id)

def list_tweet(user_id):
	conn = sqlite3.connect(path)
	api_list=[]
	cursor=conn.cursor()
	cursor.execute("SELECT * from tweets where id=?",(user_id,))
	data = cursor.fetchall()
	if len(data) == 0:
		abort(404)
	else:
		user = {}
		user['id'] = data[0][0]
		user['username'] = data[0][1]
		user['body'] = data[0][2]
		user['tweet_time'] = data[0][3]
	conn.close()
	return jsonify(user)



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


@app.route("/api/v1/users",methods=['POST'])
def create_user():
	if(not request.json  or not 'username' in request.json or not 'email' in request.json or not 'password' in request.json):
		abort(400)
	user  = {
		'username':request.json['username'],
		'email':request.json['email'],
		'name':request.json['name'],
		'password':request.json['password']
	}
	return jsonify({'sttaus':add_user(user)}),201

@app.errorhandler(400)
def invalid_request(error):
	return make_response(jsonify({'error':'Bad Request'}),400)

def add_user(new_user):
	conn = sqlite3.connect(path)
	api_list = []
	cursor = conn.cursor()
	cursor.execute("SELECT * from users WHERE username=? or emailid=?",(new_user['username'],new_user['email']))
	data = cursor.fetchall()
	if(len(data) !=0):
		abort(409)
	else:
		cursor.execute("INSERT INTO users (username,emailid,password,full_name) VALUES (?,?,?,?)",(new_user['username'],new_user['email'],new_user['password'],new_user['name']))
		conn.commit()
		return "success"
	conn.close()
	return jsonify(new_user)


@app.route("/api/v1/users",methods=['POST'])

def delete_user():
	if not request.json or not 'username' in request.json:
		abort(400)
	user = request.json['username']
	return jsonify({'status':del_user(user)}),200

def del_user(del_user):
	conn = sqlite3.connect(path)
	cursor = conn.cursor()
	cursor.execute("SELECT * from users where username=?",(del_user,))
	data = cursor.fetchall()
	if len(data)==0:
		abort(404)
	else:
		cursor.execute("DELETE from user WHERE username=?",(del_user,))
		conn.commit()
	return "success"


@app.route("/api/v1/users/<int:user_id>",methods=['PUT'])
def update_user(user_id):
	user = {}
	if not request.json:
		abort(400)
	user['id'] = user_id
	key_list = request.json.keys()
	for i in key_list:
		user[i] = request.json[i]
	print(user)

	return jsonify({"status":update_user_record(user)}),200

def update_user_record(user):
	conn = sqlite3.connect(path)
	cursor = conn.cursor()
	cursor.execute("SELECT * from users WHERE id=?",(user['id'],))
	data = cursor.fetchall()
	if(len(data)==0):
		abort(404)
	else:
		key_list = user.keys()
		for i in key_list:
			if i != "id":
				print(user,i)
				cursor.execute("""UPDATE users set {0}=? WHERE id=?""".format(i),(user[i],user['id']))
				conn.commit()
	return "success"










if __name__ == "__main__":
	app.run(host='localhost', port=5000 , debug=True)