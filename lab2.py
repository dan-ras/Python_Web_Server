#############################################################################
# Program:
#    Lab PythonWebServer, Computer Networks
#    Brother Jones, CSE354
# Author:
#    Daniel Rasmussen
# Summary:
#    This program implents a simple python web server that takes a 
#    request for a file and returns that file. If the file specified
#    by the request doesn't exist the server returns an error message.
##############################################################################
#############################################################################
#
# Changes made to my code for the Python Web Server Take-2:
#   
#   - Added 'serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)'
#     to prevent the "[Errno 48] Address already in use" error.
#   - Specified encoding type to 'ascii'
#   - Changed server console print messages when sending data.
#   - Added 'connection.close()' line 97
#
#############################################################################

# Import needed libraries
from socket import *
import sys
import os

# Based on the file extension, return the content type 
   # that is part  of the "Content-type:" header"
def contentType(filepath):
   fileExt = filepath[-3:]
  
   if fileExt == 'txt':
      return 'Content-Type: text/txt'
   elif fileExt == 'gif':
      return 'Content-Type: image/gif'
   elif fileExt == 'jpg':
      return 'Content-Type: image/jpeg'
   else:
      return 'Content-Type: text/html'

# Server Connection Setup
serverPort = int(sys.argv[1]) if len(sys.argv) == 2 else 6789
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print ("Server is running on port " , str(serverPort), "\n")

# Defining some useful strings
CRLF = "\r\n"
okmessage = 'HTTP/1.1 200 OK' + CRLF
errorMessage = '404: The file you are looking for does not exist.' + CRLF

# Main Server Loop
try:
   while 1:
      # Accept the connection and save the request to a string.
      connectionSocket, addr = serverSocket.accept()
      request = connectionSocket.recv(1024).decode()

      # Parse the token from the request string.
      parseRequest = request.split(" ")
      filename = parseRequest[1][1:]
      contType = contentType(filename) + CRLF + CRLF

      if request == "": # Ignore empty requests
         connectionSocket.close()
         continue

      # Print part of the request.
      print("Client request: ", parseRequest[0], parseRequest[1])

      # Send the header:
      connectionSocket.send(okmessage.encode('ascii'))
      connectionSocket.send(contType.encode('ascii')) 
      
      # Send the file
      try:
         f = open(filename, 'rb') # Open the file in binary.
         data = f.read(1024)
         while (data):
            print("Sending...")
            connectionSocket.send(data) # Send the file's data
            data = f.read(1024)  
         f.close() # Close the file.
         print("All packets have been sent.\n")
         
      # If the file doesn't exist send back an error message.
      except IOError:
         connectionSocket.send(errorMessage.encode('ascii'))
         print ("Returned error message to client.\n")

      connectionSocket.shutdown(1) # Inform the client that we are finished sending data
      connectionSocket.close()     # Close the connection.

# To stop the server, type 'Control-C'
except KeyboardInterrupt:
   print ("\nClosing Server")
   serverSocket.close()
   quit()