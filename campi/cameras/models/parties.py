from django.db import models
from django.utils.translation import gettext_lazy as _


class Client(models.Model):
    """
        A generic class for storing client details and executing commands on the client.
    """
    class ProtocolChoices(models.TextChoices):
        WEBRTC = 'WEBRTC', _('WebRTC')
    client_name = models.CharField(max_length=200, blank=False, null=False, default='New Client')
    ip_address = models.CharField(max_length=20, blank=False, null=False, default='0.0.0.0')
    token = models.CharField(max_length=200, blank=True, null=True, default='No Token Supplied.')
    communication_protocol = models.CharField(max_length=200, blank=False, null=False, choices=ProtocolChoices.choices, default=ProtocolChoices.WEBRTC)

    def __init__(self, ip: str, token: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ip_address = ip
        self.token = token


class Server(Client):
    """
        A server is a type of client, I suppose...
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

