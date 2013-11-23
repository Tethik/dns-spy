#!/usr/bin/python

# Just some initial values to add to the database.
# 

from pymongo import MongoClient

client = MongoClient()
db = client.dns_spy_db

if db.subdomains.count() > 0:
	print "Already inited?"
	exit(1)

db.subdomains.insert( { "name": "www" } );
db.subdomains.insert( { "name": "dev" } );
db.subdomains.insert( { "name": "test" } );
db.subdomains.insert( { "name": "office" } );

print "Added", db.subdomains.count(), "starting records."
