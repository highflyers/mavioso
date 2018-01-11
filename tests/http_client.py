import http.client
import json

connection = http.client.HTTPConnection("127.0.0.1:6666")
headers = {'Content-type': 'application/json'}

class Params:
    def __init__(self):
        self.op_code = 0
        self.latitude = 0


def execute_function(params):
    connection.request("POST", "/", json.dumps(params.__dict__), headers)
    response = connection.getresponse()
    print(response.read().decode())


def current_state():
    connection.request("GET", "/currentstate")
    response = connection.getresponse()
    print(response.read())


def main():
    current_state()
    params = Params()
    params.op_code = 3
    params.latitude = 5.4534
    execute_function(params)
    execute_function(params)


if __name__ == '__main__':
    main()