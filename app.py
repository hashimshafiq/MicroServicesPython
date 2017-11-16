from flask import Flask
from flask import jsonify
from flask import make_response
from flask import abort
from flask import request
from flask import render_template
from flask_cors import CORS, cross_origin
from flask import redirect
from flask import session
from flask import url_for
from pymongo import MongoClient
import random

import json
from time import strftime
from time import gmtime

app = Flask(__name__)
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'
CORS(app)

connection = MongoClient("mongodb://localhost:27017/")
def create_mongoDatabase():
	try:
		dbnames = connection.database_names()
		if 'cloud_native' not in dbnames:
			db = connection.cloud_native.users
			db_tweets = connection.cloud_native.tweets
			db_api = connection.cloud_native.apirelease
			db.insert({
				"email":"hashim@gmail.com",
				"id":1,
				"name":"Hashim Shafiq",
				"password":"abc123",
				"username":"hashim"
			})
			db_tweets.insert({
				"body": "New blog post,Launch your app with the AWS StartupKit!  # AWS",
				"id": 1,
				"timestamp": "2017-03-11T06:39:40Z",
				"tweetedby": "hashim"
			})
			db_api.insert({
				"buildtime": "2017-01-01 10:00:00",
				"links": "/api/v1/users",
				"methods": "get, post, put, delete",
				"version": "v1"
			})
			db_api.insert({
				"buildtime": "2017-02-11 10:00:00",
				"links": "api/v2/tweets",
				"methods": "get, post",
				"version": "v2"
			})
			print("Database Initialized")
		else:
			print("Database already initialized")
	except:
		print("Database creation failed")


@app.route("/")
def main():
    return render_template("main.html")

@app.route("/addname")
def addname():
    if request.args.get('yourname'):
        session['name'] = request.args.get('yourname')
        return redirect(url_for('main'))
    else:
        return render_template('addname.html',session=session)

@app.route("/clear")
def clearsession():
    session.clear()
    return redirect(url_for('main'))


@app.route("/adduser")
def adduser():
	return render_template('adduser.html')

@app.route("/api/v2/info")
def home_index2():
	api_list = []
	db = connection.cloud_native.apirelease
	for row in db.find():
		api_list.append(str(row))
	return jsonify({'api_version':api_list}),200

@app.route("/api/v2/tweets",methods=['GET'])
def get_tweets():
	return list_tweets()


def list_tweets():

	api_list=[]
	db = connection.cloud_native.tweets
	for row in db.find():
		api_list.append(str(row))
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
	api_list = []
	print(new_tweets)
	db_user = connection.cloud_native.users
	db_tweet = connection.cloud_native.tweets
	user = db_user.find({"username":new_tweets['username']})
	for i in user:
		api_list.append(str(i))
	if api_list == []:
		abort(404)
	else:
		db_tweet.insert(new_tweets)
		return "success"



@app.route('/api/v2/tweets/<int:id>', methods=['GET'])
def get_tweet(id):
	return list_tweet(id)

def list_tweet(user_id):

	api_list=[]
	db = connection.cloud_native.tweets
	for row in db.find({"id":user_id}):
		api_list.append(str(row))

	if api_list == []:
		abort(404)

	return jsonify({'tweet':api_list}),200



@app.route("/api/v1/info")
def home_index():
	api_list = []
	db = connection.cloud_native.apirelease
	for row in db.find():
		api_list.append(str(row))
	return jsonify({'api_version':api_list}),200

@app.route("/api/v1/users",methods=["GET"])
def get_users():
	return list_users()

def list_users():
	api_list = []
	db = connection.cloud_native.users
	for row in db.find():
		api_list.append(str(row))
	return jsonify({'user_list':api_list}),200



@app.route("/api/v1/users/<int:user_id>" ,methods=['GET'])
def get_users_details(user_id):
	return list_users_details(user_id)

def list_users_details(user_id):

	api_list = []
	db = connection.cloud_native.users
	for row in db.find({'id':user_id}):
		api_list.append(str(row))
	if api_list == []:
		abort(404)
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
		'password':request.json['password'],
		'id': random.randint(1,1000)
	}
	return jsonify({'sttaus':add_user(user)}),201

@app.errorhandler(400)
def invalid_request(error):
	return make_response(jsonify({'error':'Bad Request'}),400)

def add_user(new_user):
	api_list = []
	print(new_user)
	db = connection.cloud_native.users
	user = db.find({'$or':[{"username":new_user['username']},{"email":new_user['email']}]})
	for i in user:
		print(str(i))
		api_list.append(str(i))

	if api_list == []:
		db.insert(new_user)
		return "success"
	else:
		abort(409)
	return jsonify(new_user)


@app.route("/api/v1/users",methods=['DELETE'])
def delete_user():
	if not request.json or not 'username' in request.json:
		abort(400)
	user = request.json['username']
	return jsonify({'status':del_user(user)}),200

def del_user(del_user):
	api_list = []
	db = connection.cloud_native.users
	for i in db.find({'username':del_user}):
		api_list.append(str(i))

	if api_list == []:
		abort(404)
	else:
		db.remove({"username":del_user})
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
	api_list = []
	print(user)
	db_user = connection.cloud_native.users
	users = db_user.find_one({"id":user['id']})
	for i in users:
		api_list.append(str(i))

	if api_list == []:
		abort(409)
	else:
		db_user.update({'id':user['id']},{"$set":user},upsert=False)
		return "success"










if __name__ == "__main__":
	create_mongoDatabase()
	app.run(host='localhost', port=5000 , debug=True)