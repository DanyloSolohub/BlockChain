class HTTPError(Exception):
    error_reasons = {400: 'Bad Request',
                     404: 'Not found',
                     405: 'Method Not Allowed',
                     494: 'Request header too large',
                     505: 'HTTP Version Not Supported',
                     'unknown': 'Unknown Error'}

    def __init__(self, status, body=None):
        super()
        self.status = status
        self.reason = self.error_reasons.get(status, 'unknown')
        self.body = body
