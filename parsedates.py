import maya
import ics

DAYS_OF_WEEK = ['lun', 'mar', 'mer', 'jeu', 'ven']
TEMPORALITY = {
    'w': 7,
    'd': 1,
    'm': 4*7
}


class Event(object):

    def __init__(self, date, label, category):
        self.date = date
        self.label = label
        self.category = category


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
        occurences = [Event(first_occurence, label=self.label, category=self.category), ]
        while current < end:
            current = current.add(days=self.get_reccurence_in_days())
            occurences.append(Event(current, label=self.label, category=self.category))
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


def event_to_ical(event):
    e = ics.Event()
    e.name = event.label
    e.begin = event.date.iso8601()
    return e


def generate_events(rules):
    start = maya.parse("2018, 7, 2")
    end = start.add(days=365)
    events = []
    for rule in rules:
        events.extend(rule.get_ocurrences(start, end))
    return events


def generate_ical(events, filename, category):
    events = filter(lambda x: x.category == category, events)
    calendar = ics.Calendar(events=map(event_to_ical, events))

    with open(filename, 'w') as f:
        f.writelines(calendar)


if __name__ == '__main__':
    rules = read_rules('events.txt')
    events = generate_events(rules)

    generate_ical(events, 'prod.ical', 'prod')
    generate_ical(events, 'support.ical', 'support')

