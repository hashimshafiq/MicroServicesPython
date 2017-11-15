from flask import Flask
from flask import jsonify
import json
import sqlite3



app = Flask(__name__)

@app.route("/api/v1/info")
def home_index():
	path = "D:/OpenSource/MicroServicesPython/micro.db"
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







if __name__ == "__main__":
	app.run(host='localhost', port=5000 , debug=True)