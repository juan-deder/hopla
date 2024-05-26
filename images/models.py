from django.db.models import Model, URLField, ForeignKey, CASCADE

from tickets.models import Ticket


class Image(Model):
    url = URLField()
    ticket = ForeignKey(Ticket, on_delete=CASCADE)