from django.urls import path

from tickets.views import TicketCreateView, TicketDetailView

app_name = 'tickets'

urlpatterns = [
    path('', TicketCreateView.as_view(), name='tickets'),
    path('<int:pk>/', TicketDetailView.as_view(), name='ticket_detail'),
]
