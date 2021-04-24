from django.db import models
from collections import deque


class Queue(models.Model):
    service_name = {'change_oil': 'Change oil', 'inflate_tires': 'Inflate tires', 'diagnostic': 'Get diagnostic test'}
    line_of_cars = {'change_oil': deque(), 'inflate_tires': deque(), 'diagnostic': deque()}

    ticket_number = 0
    next_ticket = None

    def tickets(cls, service):
        line_time = {'change_oil': 2, 'inflate_tires': 5, 'diagnostic': 30}
        wait_for_line = {k: len(cls.line_of_cars[k]) * line_time[k] for k in cls.line_of_cars.keys()}
        wait_time = {'change_oil': wait_for_line['change_oil'],
                     'inflate_tires': wait_for_line['change_oil'] + wait_for_line['inflate_tires'],
                     'diagnostic': sum(wait_for_line.values())}

        Queue.ticket_number += 1
        cls.next_ticket = cls.ticket_number if cls.next_ticket is None and Queue.ticket_number > 1 else None
        cls.line_of_cars[service].append(cls.ticket_number)
        return cls.ticket_number, wait_time[service]

    @classmethod
    def next(cls):
        for v in cls.line_of_cars.values():
            if len(v) > 0:
                cls.next_ticket = v.popleft()
                return True
            else:
                continue
        cls.next_ticket = None
        return False

        # if len(cls.line_of_cars['change_oil']) > 0:
        #     cls.line_of_cars['change_oil'].popleft()
        # elif len(cls.line_of_cars['inflate_tires']) > 0:
        #     cls.line_of_cars['inflate_tires'].popleft()
        # elif len(cls.line_of_cars['diagnostic']) > 0:
        #     cls.line_of_cars['diagnostics'].popleft()
        # else:
        #     return False
        # return True
