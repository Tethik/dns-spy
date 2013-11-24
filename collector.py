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
		copy = dict()
		if len(request.form) == 0:
			return ""
		for key, val in request.form.iteritems():
			try:
				app.logger.debug(str(key) + " " + str(val))
				copy[key] = "".join(val)
			except ValueError:
				pass
		app.logger.debug("Adding " + str(copy))
		db[collection].insert(copy)
	except Exception as ex:
		app.logger.error(ex)
		return str(ex)
	return ""

if __name__ == "__main__":
	dbname = sys.argv[1]
	app.run(debug=True)
    
