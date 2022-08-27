from django.db import models

from campi.cameras.models.parties import Client, Server


class CommunicationError(Exception):
    """
        generic communication exception.
    """
    pass


class Connection(models.Model):
    """
    a model to store connection details
    """

    def __init__(self, client, server, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = client
        self.server = server

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    created_ts = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(auto_now=True)

    @property
    def is_connected(self):
        try:
            client = self.ping('CLIENT')
            server = self.ping('SERVER')
            if all([client, server]):
                return True
            else:
                return False
        except CommunicationError:
            return False

    def connect(self):
        try:
            self.initiate_connection(self.client, self.server)
            pass
        except ConnectionError:
            # log.error()
            return False

    def ping(self, recipient: str):
        response = None
        if recipient not in ['CLIENT', 'SERVER']:
            raise ConnectionError()
        try:
            response = self.send_message('ping', recipient)
            return response
        except CommunicationError:
            if response:
                # log.error()
                return response
            else:
                # log.error()
                return {'status': 'error', 'message': 'An error occurred when trying to send a message.'}

    def send_message(self, message: str, direction: str):
        # send the message
        message = message
        if direction == 'CLIENT':
            response = self.client.send(message)
        elif direction == 'SERVER':
            response = self.server.send(message)
        else:
            response = f"Invalid recipient specified. {direction}"
        return response
