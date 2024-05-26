from django.contrib.auth.models import User
from django.db.models import (Model, ForeignKey, CASCADE, CharField,
                              TextChoices, DateTimeField, PositiveSmallIntegerField)


class Ticket(Model):
    owner = ForeignKey(User, on_delete=CASCADE)
    status = CharField(default='pending', max_length=9,
                       choices=TextChoices('status', 'pending completed'))
    image_length = PositiveSmallIntegerField()
    created_datetime = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Ticket {self.id}'
