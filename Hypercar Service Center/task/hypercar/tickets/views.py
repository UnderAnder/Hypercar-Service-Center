from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import Queue

services = {'change_oil': 'Change oil', 'inflate_tires': 'Inflate tires', 'diagnostic': 'Get diagnostic test'}


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')


class MenuView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'menu.html', context={'services': services})


class TicketView(TemplateView):
    template_name = 'get_ticket.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket_number, wait_time = Queue().tickets(kwargs['service'])
        context['ticket_number'] = ticket_number
        context['wait_time'] = wait_time
        return context

class ProcessingView(View):
    def get(self, request, *args, **kwargs):
        queue_len = {services[k]: len(v) for k, v in Queue.line_of_cars.items()}
        return render(request, "processing.html", context={'queue_len': queue_len})

