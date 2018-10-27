#!/usr/bin/env python3
# An HTTP server for Udacians

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

class Udacian:
  def __init__(self, name, city, enrollment, nanodegree, status):
    self.name = name
    self.city = city
    self.enrollment = enrollment # day of the week, am or pm, session lead name 
    self.nanodegree = nanodegree
    self.status = status # ontrack, behind or critical 

  def print_udacian(self):
    return '%s is enrolled in %s studying %s in %s %s with Ms. %s, he/she is %s' % (self.name, self.city, self.nanodegree, self.enrollment[0],
                                                                              self.enrollment[1], self.enrollment[2], self.status)
memory = []

form = '''<!DOCTYPE html>
  <title>Message Board</title>
  <form method="POST">
    <textarea name="name" placeholder="Name"></textarea>
    <br>
    <textarea name="city" placeholder="City"></textarea>
    <br>
    <textarea name="enrollment" placeholder="Enrollment"></textarea>
    <br>
    <textarea name="nanodegree" placeholder="Nanodegree"></textarea>
    <br>
    <textarea name="status" placeholder="Status"></textarea>
    <br>
    <button type="submit">Press me!</button>
  </form>
  <pre>
{}
  </pre>
'''

class UdacianHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # How long was the data?
        length = int(self.headers.get('Content-length', 0))
        
        # Read the data
        data = self.rfile.read(length).decode()

        # Parse the data, extract all form fields
        params = parse_qs(data)
        name = params["name"][0]
        city = params["city"][0]
        enrollment = params["enrollment"][0]
        enrollment = tuple(enrollment.split(' ')) # cast list to tuple
        nanodegree = params["nanodegree"][0]
        status = params["status"][0]
        
        # Create Udacian object
        student = Udacian(name, city, enrollment, nanodegree, status)
        
        # Store Udacian object in memory
        memory.append(student)
        
        # Send a 303 back to the root page
        self.send_response(303)  # redirect via GET
        self.send_header('Location', '/')
        self.end_headers()

    def do_GET(self):
        # First, send a 200 OK response
        self.send_response(200)

        # Then send headers
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        # Then send the form with string representation of Udacians objects 
        mesg = form.format('\n'.join(u.print_udacian() for u in memory))
        self.wfile.write(mesg.encode())

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, UdacianHandler)
    httpd.serve_forever()