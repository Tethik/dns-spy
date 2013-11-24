#!/usr/bin/python

import sys
from flask import Flask, request
from pymongo import MongoClient
app = Flask(__name__)

dbname = ""

@app.route("/<collection>", methods=['POST'])
def collect(collection):
	try:	
		client = MongoClient()
		db = client[dbname]		
		db[collection].insert(dict(request.form))
	except Exception as ex:
		app.logger.error(ex)
		return str(ex)
	return ""

if __name__ == "__main__":
	dbname = sys.argv[1]
	app.run(debug=True)
    
