

class RocketpayException(Exception):
    def __init__(self, error):
        self.raw = error.get('status')
        self.code = error.get('status').get('code')
        self.message = error.get('status').get('message')

    def __repr__(self):
        return "<RocketpayException code={} message={}>".format(
            self.code, self.message
        )


class RocketpayParameterException(Exception):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return """<RocketpayParameterException name={}>""".format(self.name)
