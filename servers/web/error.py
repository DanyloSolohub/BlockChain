class HTTPError(Exception):

    def __init__(self, status, body=None):
        super()
        self.status = status
        self.body = body
