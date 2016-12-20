import webapp2
import cgi
import re

import urllib2


textArea = """
			<html>
				<head>
					<title>User Sign-In App</title>
					<style type="text/css">
						span {
								color:red;
								text-size:30px;
							 }
					</style>
				</head>
				<body>
					<h1>User Sign-In App<h1>
					<form action="/testUserSignIn" method="post">
						<label><h5 style="color:blue">Username
						<input type="text" name="username" value="%(username_value)s">
						</label> <span name="username-error">%(username_error)s</span>
						<br>
						<label><h5 style="color:blue">Password
						<input type="password" name="password" value="%(password_value)s">
						</label> <span name="password-error">%(password_error)s</span>
						<br>
						<label><h5 style="color:blue">Verify
						<input type="password" name="verify" value="%(verify_value)s">
						</label> <span name="verify-error">%(verify_error)s</span>
						<br>
						<label><h5 style="color:blue">Email(optional)
						<input type="text" name="email" value="%(email_value)s">
						</label> <span name="email-error">%(email_error)s</span>
						<br>
						<br>
						
						<input type="submit" name="submit-btn" value="Log In" style="text-align:center">

					</form>
					
				</body>
			</html>
			"""

# The doubled % is needed to escape for the string substitution
successText = """
				<html>
					<head>
						<style type="text/css">
							#successMessage {
												left: 50%%;
												top: 50%%;
											}
						</style>
						<title>Logged In</title>
					</head>
					
					<body>	
						<div id="successMessage">
							<p>You're Logged In %(username)s !! Welcome !!</p>
						</div>
					</body>
				</html>
			  """


def writeArea(self,htmlStr, username_error="", password_error="", verify_error="", email_error="",
			                username_value = "", password_value = "", verify_value="", email_value=""
			  ):
	self.response.write(htmlStr % {'username_error': username_error, 'password_error': password_error, 
								  'verify_error':verify_error, 'email_error' : email_error,
								  'username_value': username_value, 'password_value': password_value,
								  'verify_value': verify_value, 'email_value': email_value
								  }
						)

class UserSignIn(webapp2.RequestHandler):
	def post(self):
		# Step1: Collect all the data sent to the server
		userStr = self.request.get('username')
		passwdStr = self.request.get('password')
		verifyStr = self.request.get('verify')
		emailStr = self.request.get('email')
		
		# Boolean Values, they're gonna help me lately
		userStr_isOk = False
		passwdStr_isOk = False
		verifyStr_isOk = False
		emailStr_isOk = False
		
		#Step 2.1: Username Validation
		# Username should have:  1) Only alphanum chars
		#						 2) No spaces or blanks
		#						 3) Max-Length of 20 chars
		def validate_User(s):
			if(re.match("^[a-zA-Z0-9_-]{3,20}$", s)):
				return True
		
		userStr_isOk = validate_User(userStr)
		
		
		
					
		#Step 2.2: Password Validation
		# Passwords should be:  1) 3 chars at least
		#						2) No spaces or blanks
		#						
		def validate_Password(s):
			if(re.match("^.{3,20}$",s)):
				return True
		
		passwdStr_isOk = validate_Password(passwdStr)
		
		
					
		#Step 2.3 : Verify Validation
		# Here I perform the validation only if Password passed before
		# Of course this string has only to be identical to password
		
		
		def validate_Verify(s):
			if(passwdStr_isOk):
				if(s == passwdStr):
					return True
		
		verifyStr_isOk = validate_Verify(verifyStr)
		
					
		#Step 2.4: Verify Email
		# Email is optional. I'll check the name
		# with a regexp found on the internet.
		
		def validate_Email(s):
			if(s):
				if(re.match("^[\S]+@[\S]+.[\S]+$",s)):
					return True
			else:
				return True
		
		emailStr_isOk = validate_Email(emailStr)
		
				
					
					
		# Ok let's check now whether everything went alright
		
		if(userStr_isOk and passwdStr_isOk and verifyStr_isOk and emailStr_isOk):
			# Anything well .. Redirect to Success Page
			self.redirect('/logged_in_page' + '?username=' + cgi.escape(userStr))
		else:
			# Rewrite the form with Error messages 
			# And putting the valid values into the form (properly escaped)
			writeArea(self,textArea,  "" if userStr_isOk else "Invalid Username",
									  "" if passwdStr_isOk else "Invalid Password",
									  "" if verifyStr_isOk else "Password doesn't match",
									  "" if emailStr_isOk else "Invalid Email",
									  
									  cgi.escape(userStr) if userStr_isOk else "",
									  cgi.escape(passwdStr) if passwdStr_isOk else "",
									  #cgi.escape(verifyStr) if verifyStr_isOk else "",
									  "", # I don't want the verify string to be rewritten anyway
									  cgi.escape(emailStr) if emailStr_isOk else ""
					 )
		
class MainPage(webapp2.RequestHandler):
	def get(self):
		writeArea(self,textArea)
		
class LoggedInPage(webapp2.RequestHandler):
	def get(self):
		username = cgi.escape(self.request.get('username'))
		self.response.write(successText % {'username': username})
		#self.response.write(username)

app = webapp2.WSGIApplication([
								('/', MainPage),
								('/testUserSignIn', UserSignIn),
								('/logged_in_page', LoggedInPage)
							  ]
							  , debug = True)
