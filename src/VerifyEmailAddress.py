import re
import socket
import smtplib
import dns.resolver
import csv
import sys
import time


# Address used for SMTP MAIL FROM command  
fromAddress = 'corn@bt.com'

# Simple Regex for syntax checking
regex = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$'

cachedDomain = ''
mxRecords = None


# inputAddress = input('Please enter the emailAddress to verify:')
# addressToVerify = "sekpo22@gmail.com"

def smtpConversation(email, mxRecord):
	try:
		# Get local server hostname
		host = socket.gethostname()

		# SMTP lib setup (use debug level for full output)
		server = smtplib.SMTP()
		server.set_debuglevel(0)

		# SMTP Conversation
		server.connect(mxRecord)
		server.helo(host)
		server.mail(fromAddress)
		code, message = server.rcpt(str(email))
		server.quit()

		if code == 250:
			return 'OK'
		else:
			return 'BAD, %s' % mxRecord
	except Exception as e:
		return "Error: %s, %s" % (str(e), mxRecord)


def getMXRecordLookup(domain):
	try:
		# MX record lookup
		return dns.resolver.query(domain, 'MX')
		# print(len(records))
		# mxRecord = records[0].exchange
		# return str(mxRecord)
	except:
		return None


def checkEmailSyntax(email):
	# Syntax check
	return re.match(regex, email)

def validateEmailAddress(email):
	if checkEmailSyntax(email) != None:

		# Get domain for DNS lookup
		splitAddress = email.split('@')
		domain = str(splitAddress[1])

		global cachedDomain
		global mxRecords
		if cachedDomain == None or cachedDomain != domain:
			mxRecords = getMXRecordLookup(domain)
			cachedDomain = domain
			print('Getting new mxRecords...	|	' + domain + '	|	'+ str(mxRecords[0].exchange))
		else:
			print('Reusing mxRecords...		|	' + domain + '	|	'+ str(mxRecords[0].exchange))

		# mxRecords = getMXRecordLookup(domain)
		if mxRecords != None and len(mxRecords) > 0:
			# for record in mxRecords:
			# 	exchange = str(record.exchange)
			# 	result = smtpConversation(email, exchange)
			# 	print(exchange + " : " + result)

			exchange = str(mxRecords[0].exchange)
			# return smtpConversation(email, exchange)
			return 'OK'
		else:
			return 'Missing MX record'
	else:
		return 'Bad syntax'

def getCurrentTime():
	return int(round(time.time() * 1000))

#Read from file line by line
# with open("input.csv") as f:
# 	index = 0
# 	for line in f:
# 		#extract email value
# 		print(index)
# 		index+=1


t1 = getCurrentTime()

with open('output.csv', 'w') as outputFile:
	thedatawriter = csv.writer(outputFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

	#read file
	f = open("input.csv")
	try:
		reader = csv.reader(f)
		for row in reader:
			emailToVerify = row[1]
			# row.append('OK')
			row.append(validateEmailAddress(emailToVerify))
			thedatawriter.writerow(row)
			# print(emailToVerify + ": " + validateEmailAddress(emailToVerify))
	finally:
		f.close()
		outputFile.close()

print("Took: " + str(getCurrentTime() - t1))




