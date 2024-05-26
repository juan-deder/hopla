from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import FileField
from django.views.generic import CreateView
from images.models import Image
from images.tasks import upload_image
from tickets.models import Ticket


class ImageCreateView(LoginRequiredMixin, CreateView):
    model = Image
    fields = ['ticket']
    success_url = '/images'

    def form_valid(self, form):
        ticket = form.cleaned_data['ticket']
        if ticket.image_set.count() == ticket.image_length:
            form.add_error(
                None, 'You have reached the maximum number of images')
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['ticket'].queryset = Ticket.objects.filter(
            owner=self.request.user)
        form.fields['image'] = FileField()

        def save(func):
            def wrapped():
                image = func()
                upload_image.delay(image.id, form.cleaned_data['image'].read())
                ticket = form.cleaned_data['ticket']
                if ticket.image_set.count() == ticket.image_length:
                    ticket.status = 'completed'
                    ticket.save()
                return image
            return wrapped

        form.save = save(form.save)
        return form
