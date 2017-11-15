import http.client
import json

connection = http.client.HTTPConnection("127.0.0.1:1234")
headers = {'Content-type': 'application/json'}

def execute_function(function_name, **kwargs):
    args = json.dumps(kwargs)

    connection.request("POST", "/"+function_name, args, headers)
    response = connection.getresponse()
    print(response.read().decode())

def current_state():
    connection.request("GET", "/currentstate")
    response = connection.getresponse()
    print(response.read())

def main():
    current_state()
    execute_function("arm")
    execute_function("takeoff", alt=50)

if __name__ == '__main__':
    main()