# Python 2.7!

# request forever
# GET D:/wwwroot/webroot/index.html HTTP/1.1\r\n
# HTTP Server Shell
# Purpose: Provide a basis for Ex. 4.4

import socket
import os.path
import socket

IP = '127.0.0.1'
PORT = 80
SOCKET_TIMEOUT = 100000
DEFAULT_URL = r'\index.html'
DEFAULT_URL2 = r'D:\wwwroot\webroot'
REDIRECTION_DICTIONARY = {}
FORBIDDEN_DICTIONARY = {}
VERSION = 'HTTP/1.1'


def get_file_data(url, file_type):
    file_path = DEFAULT_URL2 + url.replace('/', '\\')
    file_content = ''
    if file_type == 'text/html; charset=utf-8':
        try:
            filey = open(file_path)
            file_content = filey.read()
        except IOError:
            pass
    else:
        try:
            filey = open(file_path, 'rb')
            file_content = filey.read()
        except IOError:
            pass
    return file_content


def handle_client_request(resource, client_socket):
    url = resource
    if resource == '' or resource == '/':
        url = DEFAULT_URL

    # PROBLEMS SECTION
    stat = ['200', 'OK']
    if url in REDIRECTION_DICTIONARY:
        stat = ['302', 'Moved Temporarily']
    elif url in FORBIDDEN_DICTIONARY:
        stat = ['403', 'Forbidden']
    elif os.path.isfile(url):
        stat = ['404', 'Not Found']

    filetype = url.split('.')[-1]
    if filetype == 'ico':
        filetype = 'image/x-icon;'
    elif filetype == 'html':
        filetype = 'text/html; charset=utf-8'
    elif filetype == 'jpg':
        filetype = 'image/jpeg;'
    elif filetype == 'png':
        filetype = 'image/png;'
    elif filetype == 'js':
        filetype = 'text/javascript;'
    elif filetype == 'css':
        filetype = 'text/css;'
    else:
        filetype = 'unknown (' + filetype + ')'

    data = get_file_data(url, filetype)
    http_header = VERSION + ' ' + stat[0] + ' ' + stat[1] + '\r\n' \
        + 'Content-Type: ' + filetype + '\r\n'\
        + 'Content-Length: ' + str(len(data)) + '\r\n' \
        + '\r\n'
    http_response = http_header + data
    client_socket.send(http_response)


def validate_http_request(request):
    request = request.split(' ', 2)
    print request
    # request[0] = GET
    # request[1] = URL
    # request[2] = HTTP/1.1\r\n
    if "GET" in request[0] and "HTTP/1.1\r\n" in request[2]:
        return True, request[1]
    return False, request[1]


def handle_client(client_socket):
    print 'Client connected'
    while True:
        client_request = client_socket.recv(1024)
        valid_http, resource = validate_http_request(client_request)
        if valid_http:
            print 'Got a valid HTTP request'
            handle_client_request(resource, client_socket)
        else:
            print 'Error: Not a valid HTTP request.'
            break
    print 'Closing connection'
    client_socket.close()


def main():
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen(10)
    print "Listening for connections on port %d" % PORT

    while True:
        client_socket, client_address = server_socket.accept()
        print 'New connection received'
        client_socket.settimeout(SOCKET_TIMEOUT)
        handle_client(client_socket)


if __name__ == "__main__":
    main()
