import maya
from jinja2 import Environment, FileSystemLoader
import os.path
import codecs
import json

TEMPLATES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
DAYS_OF_WEEK = ['lun', 'mar', 'mer', 'jeu', 'ven']
TEMPORALITY = {
    'w': 7,
    'd': 1,
    'm': 4*7
}
COLORS = {
    'prod': 'blue',
    'support': '#257e4a'
}


class Event(object):

    def __init__(self, date, label, category, duration=None, all_day=None):
        self.date = date
        self.duration = duration
        self.all_day = all_day
        self.label = label
        self.category = category

    @classmethod
    def from_rule(cls, rule, date):
        kwargs = {}

        if rule.hours == 'allday':
            kwargs['all_day'] = True

        elif rule.hours:
            start, end = rule.hours.split('-')
            start = int(start[0:-1])
            end = int(end[0:-1])
            date = date.add(hours=start)
            kwargs['duration'] = end - start

        return cls(date, rule.label, rule.category, **kwargs)

    def to_ical(self):
        from pdb import set_trace; set_trace()
        e = ics.Event(self.label, self.date.iso8601())
        if self.duration:
            e.duration = self.duration

        if self.all_day:
            e.make_all_day()

        return e

    def to_fullcalendar_dict(self):
        return {
            'title': self.label,
            'start': self.date.iso8601(),
            'color': COLORS[self.category]
        }



class Rule(object):
    def __init__(self, dow, week, hours, label, recurrance, category):
        self.dow = dow
        self.week = int(week)
        self.hours = hours
        self.label = label
        self.recurrance = recurrance
        self.category = category

    def get_reccurence_in_days(self):
        number = int(self.recurrance[0:-1])
        temporality = TEMPORALITY[self.recurrance[-1]]
        return number * temporality

    def get_ocurrences(self, start, end):
        # First, set the event relative to a given date.
        # start needs to be a monday.
        days_delta = (self.week - 1) * 7 + DAYS_OF_WEEK.index(self.dow)
        first_occurence = start.add(days=days_delta)
        current = first_occurence
        occurences = [Event.from_rule(self, first_occurence), ]
        while current < end:
            current = current.add(days=self.get_reccurence_in_days())
            occurences.append(Event.from_rule(self, current))
        return occurences



def parse_rule(text):
    args = text.split(',')
    return Rule(*map(str.strip, args))


def read_rules(filename):
    rules = []

    with open(filename) as f:
        for line in f.readlines():
            if len(line) < 3 or line.startswith('#'):
                pass
            else:
                rules.append(parse_rule(line.strip('\n')))
    return rules




def generate_events(rules):
    start = maya.parse("2018, 7, 2")
    end = start.add(days=365)
    events = []
    for rule in rules:
        events.extend(rule.get_ocurrences(start, end))
    return events


def generate_ical(events, filename, category):
    events = filter(lambda x: x.category == category, events)
    calendar = ics.Calendar(events=[e.to_ical() for e in events])

    with open(filename, 'w') as f:
        f.writelines(calendar)


def render_template(output_path, tpl_name, filename, **options):
    env = Environment(loader=FileSystemLoader(TEMPLATES_PATH))
    template = env.get_template(tpl_name)
    output = template.render(**options)

    full_path = os.path.join(output_path, filename)

    with codecs.open(full_path, 'w+', encoding='utf-8') as f:
        f.write(output)


def generate_fullcalendar(events, output_path):

    render_template(
        output_path, 'index.html', 'index.html',
        events=json.dumps([e.to_fullcalendar_dict() for e in events]), defaultdate='2018-07-01'
    )


if __name__ == '__main__':
    rules = read_rules('events.txt')
    events = generate_events(rules)
    generate_fullcalendar(events, 'app')

    # generate_ical(events, 'prod.ical', 'prod')
    # generate_ical(events, 'support.ical', 'support')
