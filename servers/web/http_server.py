import socket
from datetime import datetime
from email.parser import Parser

from servers.web.response import Response
from servers.web.error import HTTPError
from servers.web.request import Request


class BaseHttpServer:
    MAX_LINE = 2 ** 6 * 2 ** 10
    MAX_HEADERS = 100
    ISO_8859_1 = 'iso-8859-1'
    UTF_8 = 'utf-8'
    DEFAULT_CONTENT_TYPE = 'application/json; charset=utf-8'
    DATE = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __init__(self, host='127.0.0.1', port=2021, server_name=None):
        self._host = host
        self._port = port
        self._server_name = server_name
        self.server_socket = socket.socket(socket.AF_INET,  # задамем семейство протоколов 'Интернет' (INET)
                                           socket.SOCK_STREAM,  # задаем тип передачи данных 'потоковый' (TCP)
                                           proto=0)  # выбираем протокол 'по умолчанию' для TCP, т.е. IP

    def serve_forever(self):
        self.server_socket.bind((self._host, self._port))
        self.server_socket.listen(10)

        while True:
            client_socket, _ = self.server_socket.accept()
            try:
                self.serve_client(client_socket)
            except Exception as e:
                print(f'Client serving failed, error - {e}')
            finally:
                client_socket.close()

    def serve_client(self, client_socket):
        try:
            request = self.parse_request(client_socket)
            response = self.handle_request(request)
            self.send_response(client_socket, response)
        except (Exception, HTTPError) as e:
            self.send_error(client_socket, e)
        else:
            request.rfile.close()
        finally:
            client_socket.close()

    def parse_request(self, client_socket):
        rfile = client_socket.makefile('rb')
        method, target, version = self.parse_request_line(rfile)
        headers = self.parse_headers(rfile)
        host = headers.get('Host')
        if not host:
            raise HTTPError(400, 'Host header is missing')
        if host not in (self._server_name,
                        f'{self._server_name}:{self._port}',
                        f'{self._host}:{self._port}'):
            raise HTTPError(404)
        return Request(method, target, version, headers, rfile)

    def parse_request_line(self, rfile):
        raw = rfile.readline(self.MAX_LINE + 1)
        if len(raw) > self.MAX_LINE:
            raise HTTPError(400, 'Request line is too long')

        request_line = str(raw, encoding=self.ISO_8859_1)
        words = request_line.split()
        if len(words) != 3:
            raise HTTPError(400, 'Malformed request line')

        method, target, version = words
        if version != 'HTTP/1.1':
            raise HTTPError(505)
        return method, target, version

    def parse_headers(self, rfile):
        headers = []
        while True:
            line = rfile.readline(self.MAX_LINE + 1)
            if len(line) > self.MAX_LINE:
                raise HTTPError(494)

            if line in (b'\r\n', b'\n', b''):
                break

            headers.append(line)
            if len(headers) > self.MAX_HEADERS:
                raise HTTPError(494, 'Too many headers')

        sheaders = b''.join(headers).decode(self.ISO_8859_1)
        return Parser().parsestr(sheaders)

    def handle_request(self, request):
        handlers = {'GET': self.get,
                    'POST': self.post,
                    'PUT': self.put,
                    'PATCH': self.patch,
                    'DELETE': self.delete}
        method_handler = handlers.get(request.method)
        if method_handler:
            return method_handler(request)
        raise HTTPError(404)

    def send_response(self, client_socket, response):
        wfile = client_socket.makefile('wb')
        status_line = f'HTTP/1.1 {response.status} {response.reason}\r\n'
        wfile.write(status_line.encode(self.ISO_8859_1))

        if response.headers:
            for (key, value) in response.headers:
                header_line = f'{key}: {value}\r\n'
                wfile.write(header_line.encode(self.ISO_8859_1))
        else:
            header_line = f'Content-Type: {self.DEFAULT_CONTENT_TYPE}\r\n'
            header_line += f'Date: {self.DATE}\r\n'
            if response.body:
                header_line += f'Content-Length: {len(response.body)}\r\n'
            wfile.write(header_line.encode(self.ISO_8859_1))
        wfile.write(b'\r\n')

        if response.body:
            wfile.write(response.body.encode(self.UTF_8))

        wfile.flush()
        wfile.close()

    def send_error(self, client_socket, error):
        try:
            status = error.status
            body = error.body
        except AttributeError:
            status = 500
            body = 'Internal Server Error'
        response = Response(status=status, body=body)
        self.send_response(client_socket, response)

    def get(self, request):
        # return Response(200, body=json.dumps({'u are pussy': 'yes'}))
        raise HTTPError(405, f'Method {request.method} not allowed')

    def post(self, request):
        raise HTTPError(405, f'Method {request.method} not allowed')

    def put(self, request):
        raise HTTPError(405, f'Method {request.method} not allowed')

    def patch(self, request):
        raise HTTPError(405, f'Method {request.method} not allowed')

    def delete(self, request):
        raise HTTPError(405, f'Method {request.method} not allowed')
