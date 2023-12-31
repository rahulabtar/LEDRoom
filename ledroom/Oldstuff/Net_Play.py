#http websites uses response and requests
#This response includes the HTTP status line, headers, and the response body. 
#The response body can contain the output generated by the PHP script, which can be HTML, 
#JSON, XML, or any other content type.
import time
from http.server import BaseHTTPRequestHandler, HTTPServer 

#Below class inherits from the BaseHTTPRequestHandler class
#In order to properly override methods we must overide the given methods
class Exhttp(BaseHTTPRequestHandler): 
    def do_GET(self): #what to do when a get request is recieved
        self.send_response(200) #Sends a response to the requester of the HTTP
        #200 is a certain code meaning everything is ok! 404 for example is not found
        self.send_header("Content Type","text/html") #clarifies the content type for later
        self.end_headers() #ends header section
        #html code we want to display
        html = '''
<html>
   <body style="width:960px; margin: 20px auto;">
   <h1>Welcome to Rahul's Raspberry Pi LED Strip Controller</h1>
   </body>
</html>
'''
        self.wfile.write(bytes(html,"utf-8")) #sends html code back to requester in bytes encoded in utf-8

host_name = '10.69.0.114'  # IP Address of Raspberry Pi
host_port = 8000 #like a given port of a dock, allows hosts to have unlimited ports / parts of a website :)

server = HTTPServer((host_name,host_port),Exhttp) #creates object of HTTPSERVER class with Exhttp child class
print("server is running")

server.serve_forever() #this causes code to stop here at line 32, as the server is opened and listening for request forever
server.server_close() #this would close the server, but doesn't happen because above repeats forever
print("server stopped")