import webapp2
import cgi

#appState = ""

textArea = """
			<html>
				<head>
					<title>ROT13</title>
				</head>
				<body>
					<h1>Convert the underlying message with ROT13 cypher<h1>
					<form action="/testform" method="post" id="form1">
						<!--<input type="textarea" rows="10" cols="30">-->
						<textarea name="text" form="form1" rows="10" cols="30">%(converted)s</textarea>
						<input type="submit" value="%(submitValue)s" name="submit-btn">
					</form>
					
				</body>
			</html>
			"""



class ROT13(webapp2.RequestHandler):
	
	def post(self):
		
		# Perform the ROT13 cyphers
		def toRot13(st):
			# Have a mutable list repr of the string
			listRepr = list(st)
			# Keep track of the place we are in the list
			currentIndex=0
			
			
			for char in listRepr:
				# Case #1 : Digit
				if(ord(char) >= 48 and ord(char) <= 57):
					if(ord(char)+13 > 57):
						
				
				if(char.isalnum()):
					asciiCode = ord(char)+13
					# Problem 1: if the resulting ascii value is betwenn 91 and 96
					# the encoded char becomes a punctuation value, so it will not be
					# decode on a new post request.
					# I decided simply to add 10
					
					## TO-DO
					
					
					# If my ascii code is over 126 we'll have an invalid char
					# 126 - ord(char) is the offset with the last value
					# i want to be hitted (char '~')
					# So in those cases I start again from 97 (let 'a') and add the remaining
					# offset steps
					if(126 - ord(char) < 13):
						
						listRepr[currentIndex] = chr(97 + (13 - (126-ord(char))  ) )
					else:
						listRepr[currentIndex] = chr( asciiCode )
				
				currentIndex += 1
			
			# We want a str type to return
			return "".join(listRepr)
			
				
		# Perform a decoding through ROT13	
		def toNormal(st):
			# Have a mutable list representation of the string
			listRepr = list(st)
			# Keep track of the place we are in the list
			currentIndex=0
			for char in listRepr:
				
				if(char.isalnum()):
					
					## TO-DO Treat here non-valid ascii codes
					listRepr[currentIndex] = chr( ord(char)-13 )
				
				currentIndex += 1
			
			# We want a str type to return
			return "".join(listRepr)
		
		
		userStr = str(self.request.get('text'))
		
		#self.response.write(appState)
		state = self.request.get("submit-btn")

		if(state == 'Cypher'):
			convertedStr = toRot13(userStr)
			
			escapedStr = cgi.escape(convertedStr)
			self.response.write(textArea % {'converted' : escapedStr, 'submitValue' : 'Decode'})
			
		else:
			convertedStr = toNormal(userStr)
			
			escapedStr  = cgi.escape(convertedStr)
			self.response.write(textArea % {'converted': escapedStr, 'submitValue' : 'Cypher'})
		
		
class MainPage(webapp2.RequestHandler):
	def get(self):
		#appState = 'normal'
		self.response.write(textArea % {'converted' : '', 'submitValue' : 'Cypher'})

app = webapp2.WSGIApplication([
								('/', MainPage),
								('/testform', ROT13)
							  ]
							  , debug = True)
