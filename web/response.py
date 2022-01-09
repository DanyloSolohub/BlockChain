class Response:
    response_reason = {200: 'OK',
                       201: 'Created',
                       204: 'No Content',
                       400: 'Bad Request',
                       404: 'Not found',
                       405: 'Method Not Allowed',
                       494: 'Request header too large',
                       500: 'Internal Server Error',
                       505: 'HTTP Version Not Supported',
                       'unknown': 'Unknown Status'}

    def __init__(self, status, headers=None, body=None):
        self.status = status
        self.reason = self.response_reason.get(status, 'unknown')
        self.headers = headers
        self.body = body
