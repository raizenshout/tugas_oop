# openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes
from http.server import HTTPServer, SimpleHTTPRequestHandler
import ssl
from io import BytesIO
import os
class MyHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Welcome aboard!')
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'This is a POST request. ')
        response.write(b'Received: ')
        response.write(body)
        self.wfile.write(response.getvalue())
if __name__ == '__main__':
    PORT = 4443
    httpd = HTTPServer(('localhost', 4443), MyHTTPRequestHandler)
    httpd.socket = ssl.wrap_socket(httpd.socket,
            keyfile=os.getcwd() + "/key.pem",
            certfile=os.getcwd() + "/cert.pem",
            server_side=True)
    print("serving at port", PORT)
    httpd.serve_forever()