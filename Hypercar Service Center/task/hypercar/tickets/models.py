from django.db import models
from collections import deque


class Queue(models.Model):
    service_name = {'change_oil': 'Change oil', 'inflate_tires': 'Inflate tires', 'diagnostic': 'Get diagnostic test'}
    line_of_cars = {'change_oil': deque(), 'inflate_tires': deque(), 'diagnostic': deque()}

    ticket_number = 0

    def tickets(self, service):
        line_time = {'change_oil': 2, 'inflate_tires': 5, 'diagnostic': 30}
        wait_for_line = {k: len(Queue.line_of_cars[k]) * line_time[k] for k in Queue.line_of_cars.keys()}
        wait_time = {'change_oil': wait_for_line['change_oil'],
                     'inflate_tires': wait_for_line['change_oil'] + wait_for_line['inflate_tires'],
                     'diagnostic': sum(wait_for_line.values())}

        Queue.ticket_number += 1
        Queue.line_of_cars[service].append(Queue.ticket_number)
        return self.ticket_number, wait_time[service]
