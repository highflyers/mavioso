from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import json


class Server(HTTPServer):
    def serve_forever(self, drone, cmd_queue, mav_lock):
        self.RequestHandlerClass.drone = drone
        self.RequestHandlerClass.cmd_queue = cmd_queue
        self.RequestHandlerClass.mavLock = mav_lock
        HTTPServer.serve_forever(self)


class ServerHandler(BaseHTTPRequestHandler):
    drone = None
    cmd_queue = None
    mavLock = None

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self.mavLock.acquire()
        ret = self.drone.currentstate()
        self.mavLock.release()

        self._set_headers()
        self.wfile.write(json.dumps(ret))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        function_name = self.path.replace("/", "")
        length = int(self.headers.getheader('content-length'))
        data = self.rfile.read(length)

        self.cmd_queue.put([str(data),function_name])
        
        self._set_headers()
        self.wfile.write(json.dumps({"status": 1}))


def run(drone, cmd_queue, mav_lock, port=80):
    server_address = ('', port)
    httpd = Server(server_address, ServerHandler)
    print("Starting httpd...")
    httpd.serve_forever(drone, cmd_queue, mav_lock)


if __name__ == "__main__":
    run(None, None, None, 6666)
