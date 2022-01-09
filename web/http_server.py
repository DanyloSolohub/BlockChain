import socket
from email.parser import Parser

from web.response import Response
from web.error import HTTPError
from web.request import Request


class BaseHttpServer:
    MAX_LINE = 2 ** 6 * 2 ** 10
    MAX_HEADERS = 100

    def __init__(self, host='127.0.0.1', port=2021, server_name=None):
        self._host = host
        self._port = port
        self._server_name = server_name
        self.server_socket = socket.socket(socket.AF_INET,  # задамем семейство протоколов 'Интернет' (INET)
                                           socket.SOCK_STREAM,  # задаем тип передачи данных 'потоковый' (TCP)
                                           proto=0)  # выбираем протокол 'по умолчанию' для TCP, т.е. IP

    def serve_forever(self):
        self.server_socket.bind((self._host, self._port))
        self.server_socket.listen()

        while True:
            client_socket, _ = self.server_socket.accept()
            try:
                self.serve_client(client_socket)
            except Exception as e:
                print(f'Client serving failed, error - {e}')
            finally:
                print('you here ')
                client_socket.close()

    def serve_client(self, client_socket):
        request = ''
        try:
            request = self.parse_request(client_socket)
            response = self.handle_request(request)
            self.send_response(client_socket, response)
        except Exception as e:
            self.send_error(client_socket, e)
        finally:
            if isinstance(request, Request):
                request.rfile.close()
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

        req_line = str(raw, 'iso-8859-1')
        words = req_line.split()
        if len(words) != 3:
            raise HTTPError(400, 'Malformed request line')

        method, target, ver = words
        if ver != 'HTTP/1.1':
            raise HTTPError(505)
        return method, target, ver

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

        sheaders = b''.join(headers).decode('iso-8859-1')
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
        raise HTTPError(404, 'Not found')

    def send_response(self, client_socket, response):
        wfile = client_socket.makefile('wb')
        status_line = f'HTTP/1.1 {response.status} {response.reason}\r\n'
        wfile.write(status_line.encode('iso-8859-1'))

        if response.headers:
            for (key, value) in response.headers:
                header_line = f'{key}: {value}\r\n'
                wfile.write(header_line.encode('iso-8859-1'))

        wfile.write(b'\r\n')

        if response.body:
            wfile.write(response.body)

        wfile.flush()
        wfile.close()

    def send_error(self, conn, err):
        try:
            status = err.status
            reason = err.reason
            body = (err.body or err.reason).encode('utf-8')
        except AttributeError:
            status = 500
            reason = b'Internal Server Error'
            body = b'Internal Server Error'
        resp = Response(status, reason,
                        [('Content-Length', len(body))],
                        body)
        self.send_response(conn, resp)

    def get(self, request):
        raise HTTPError(405, f'Method {request.method} not allowed')

    def post(self, request):
        raise HTTPError(405, f'Method {request.method} not allowed')

    def put(self, request):
        raise HTTPError(405, f'Method {request.method} not allowed')

    def patch(self, request):
        raise HTTPError(405, f'Method {request.method} not allowed')

    def delete(self, request):
        raise HTTPError(405, f'Method {request.method} not allowed')


if __name__ == '__main__':
    server = BaseHttpServer()
    # try:
    server.serve_forever()
    # except KeyboardInterrupt:
    #     pass
