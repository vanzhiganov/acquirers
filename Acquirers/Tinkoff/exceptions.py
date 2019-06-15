

class TinkoffException(Exception):
    def __init__(self, error):
        self.raw = error
        self.code = error['ErrorCode']
        self.message = error['Message']
        self.details = error['Details']
        self.success = error['Success']

    def __repr__(self):
        return "<TinkoffException success={} code={} message={} details={}>".format(
            self.success, self.code, self.message, self.details
        )
