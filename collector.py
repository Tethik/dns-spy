#!/usr/bin/python

import sys
from flask import Flask, request
from pymongo import MongoClient
app = Flask(__name__)

dbname = ""

@app.route("/subdomains", methods=['POST'])
def collect():
	try:	
		client = MongoClient()
		db = client[dbname]		
		if len(request.form) == 0:
			return ""
		
		name = request.form.get("name")				
		app.logger.debug("Updating " + str(name))				
		db["subdomains"].update({ "name": name }, {"$inc": { "count": 1 }}, upsert=True)
		
	except Exception as ex:
		app.logger.error(ex)
		return str(ex)
	return ""

if __name__ == "__main__":
	dbname = "dns_spy_db"
	app.run(debug=True, port=5337)
    
