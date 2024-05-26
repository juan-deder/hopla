from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView

from tickets.models import Ticket


class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    fields = ['image_length']
    success_url = '/tickets'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        context = Ticket.objects.filter(owner=request.user)
        get_response = super().get(request, *args, **kwargs)
        fields = ["status", "created_datetime__gte", "created_datetime__lte"]
        context = context.filter(**{
            k: request.GET.get(k) for k in fields if request.GET.get(k)})
        for field in fields:
            get_response.context_data[field] = request.GET.get(field)

        get_response.context_data['tickets'] = context
        return get_response

class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket
    template_name = 'tickets/ticket_detail.html'

    def get_queryset(self):
        return Ticket.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = context['ticket'].image_set.all()
        return context