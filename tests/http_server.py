import sys
sys.path.append(r"C:\Python27amd64\Lib")
sys.path.append(r"C:\maciej\projects\mavioso")

import sys
import clr
import MissionPlanner
clr.AddReference("MAVLink")
from System import Byte
import MAVLink
from MAVLink import mavlink_command_long_t
from MAVLink import MAV_CMD
import MAVLink
clr.AddReference("MissionPlanner.Utilities") # includes the Utilities class
from MissionPlanner.Utilities import Locationwp

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer

import mavioso.MAV
import mavioso.MAV_server_side
import tests.context
import logging
import json

drone_ll = mavioso.MAV.MAV(Script, MAV, MAVLink, cs)
drone = mavioso.MAV_server_side.MAV_server_side(drone_ll)

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        print("GET: " + self.path)
        self._set_headers()
        if(self.path == "/currentstate"):
            self.wfile.write(json.dumps(drone.currentstate()))
        else:
            # TODO: return 404
            self.wfile.write(json.dumps({}))

    def do_HEAD(self):
        print("HEAD")
        self._set_headers()
        
    def do_POST(self):
        print("POST: " + self.path)
        function_name = self.path.replace("/", "")
        function_to_call = getattr(drone, function_name)
        length = int(self.headers.getheader('content-length'))
        data = self.rfile.read(length)
        function_kwargs = json.loads(data)
        print(function_to_call)
        print(function_kwargs)
        status = function_to_call(**function_kwargs)
        self._set_headers()
        self.wfile.write(json.dumps({"status": int(status)}))
        
def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

run(port=1234)