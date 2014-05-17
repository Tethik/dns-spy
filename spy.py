#!/usr/bin/python

import sys, gflags
from pymongo import MongoClient
import pymongo
import dns.query
import dns.zone
import dns.resolver
import dns.rdtypes.IN
import dns.rdtypes.ANY
import dns.name
import random, string

__program__         = 'dns-spy'
__version__         = 'v0.2331'
__author__          = 'Joakim Uddholm'
__doc__             = """
USAGE: %s <domain>

Example: %s google.com

"""

FLAGS = gflags.FLAGS
# allow mixing of commands and options
FLAGS.UseGnuGetOpt()

gflags.DEFINE_bool("help", None, "Show this help")
#gflags.DEFINE_string("axfr", False, "Attempt to zone transfer")
gflags.DEFINE_bool("dtypes", True, "Bruteforce on dns types")
gflags.DEFINE_bool("axfr", False, "Attempt to zone transfer")
#gflags.DEFINE_integer("maxdepartures", 10, "Max amount of departures to show")
gflags.DEFINE_bool("dictionary", True, "Perform dictionary based guessing")
#gflags.DEFINE_multistring("types", ['bus','train','metro','tram'], "Which types of transit to include. Possible: bus, train, metro or tram")

def Usage():
	print __program__
	print __version__
	print __author__
	print __doc__ % sys.argv[0]
	exit(1)
		

def DTypes(domain):
	for _type in dns.rdtypes.ANY.__all__ + dns.rdtypes.IN.__all__:
		try:
			#print _type
			answers = dns.resolver.query(domain, _type)
			for rdata in answers:
				print _type, rdata
		except:
			pass # No Answer.

def Dictionary(domain):
	client = MongoClient()
	db = client.dns_spy_db
	
	# check wildcard.
	r = ""
	for _ in range(12):
		r += random.choice(string.lowercase)
	q = r + "." + domain
	wildcard_ips = list()
	
	try:
		answers = dns.resolver.query(q)
		
		for ans in answers:
			wildcard_ips.append(ans)
			print "*."+domain, ans
	except:
		pass
	
	# for now hardcoded.	
	subs = db.subdomains.find().sort('count', pymongo.DESCENDING)
	for sub in subs:				
		try:
			q = sub["name"] + "." + domain
			answers = dns.resolver.query(q)
			for rdata in answers:
				#print q, rdata
				if(rdata not in wildcard_ips):
					print q, rdata
				
		except:
			pass # No match.
	

if __name__ == '__main__':
	try:
		sys.argv = FLAGS(sys.argv)  # parse flags		
	except gflags.FlagsError, e:
		print '%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS)
		sys.exit(1)
	
	if(FLAGS.help):
		Usage()
		
	domain = sys.argv[1]
	
	if FLAGS.dtypes:
		print "# Performing lookup based on domain types."
		DTypes(domain)
		print
	
	#if FLAGS.axfr:
		# We need to get external ip if we want to attempt a zone transfer here.
		# Todo.
	#	z = dns.zone.from_xfr(dns.query.xfr('127.0.0.1', 'ns-1176.awsdns-19.org'))
	#	names = z.nodes.keys()
	#	names.sort()
	#	for n in names:
	#		print z[n].to_text(n)
			
	if FLAGS.dictionary:
		print "# Performing dictionary lookup"
		Dictionary(domain)
		print
		
			

