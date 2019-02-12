from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib
from urllib.parse import *
from io import BytesIO


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def doPathParse(self,path):
        parsePath = urlparse(path)
        filePath = parsePath.path
        fileQuery = parsePath.query
        fileDecode = urllib.parse.parse_qs(fileQuery)
        result = {"parse":parsePath, "path":filePath , "query": fileQuery, "decodeQuery": fileDecode}
        return result


    def do_GET(self):
        print ("\tHeaders:")
        print (self.headers);
        print ("\n")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!\n')

    def do_POST(self):
        print ("\tHeaders:")
        print (self.headers);
        print ("\n")
        content_length = int(self.headers['Content-Length'])
        params = {}
        if content_length > 0:
           body = self.rfile.read(content_length)
           #print("\tBody:\n")
           #print(body)
           params = urllib.parse.parse_qs(body.decode())
        else:
           pathParse = self.doPathParse(self.path)
           params = pathParse["decodeQuery"];
           #print ("\tPathParse:")
           #print (pathParse)
           #print ("\n")
           body = pathParse["query"].encode()
        print ("Params: ");
        for p,v in params.items():
           print (" -",p,"=>",v)
        print (" ------------------- --------------------\n")
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'This is POST request. ')
        response.write(b'Received: ')
        response.write(body)
        response.write(b'\n')
        self.wfile.write(response.getvalue())


httpd = HTTPServer(('localhost', 61000), SimpleHTTPRequestHandler)
httpd.serve_forever()
