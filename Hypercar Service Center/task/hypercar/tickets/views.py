from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')


class MenuView(View):
    services = {'change_oil': 'Change oil', 'inflate_tires': 'Inflate tires', 'diagnostic': 'Get diagnostic test'}

    def get(self, request, *args, **kwargs):
        return render(request, 'menu.html', context={'services': self.services})


class TicketView(TemplateView):
    template_name = 'get_ticket.html'
    line_of_cars = {'change_oil': [], 'inflate_tires': [], 'diagnostic': []}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = kwargs['service']
        context['service'] = service
        line_time = {'change_oil': 2, 'inflate_tires': 5, 'diagnostic': 30}
        wait_for_line = {k: len(self.line_of_cars[k]) * line_time[k] for k in self.line_of_cars.keys()}
        wait_time = {'change_oil': wait_for_line['change_oil'],
                     'inflate_tires': wait_for_line['change_oil'] + wait_for_line['inflate_tires'],
                     'diagnostic': sum(wait_for_line.values())}
        ticket_number = len(self.line_of_cars[service]) + 1
        self.line_of_cars[service].append(ticket_number)
        context['ticket_number'] = ticket_number
        context['wait_time'] = wait_time[service]
        return context
