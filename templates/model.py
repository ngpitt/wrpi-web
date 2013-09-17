# This is the function called by the WSGI handler
def application(environ, start_response):

	# Output is a string (use yield, it's faster)
	yield output