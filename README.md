# Recurring events planifier

This is a small utility to generate calendars for recurring events. I've made
it because I found it very hard to have events that are interdependent to each
others. For instance in a brewery, I need to brew a batch of beer on a specific
day, and once this is done, a set of events need to be done relatively to the
date of the brew.

With other tools such as online calendars, I need to move everything manually,
and it's a real pain. Also, recurring events really seem to make sense for me
using this tool.

This tool is intended to generate a view at a specific point in time, and from
it you can add the events in a calendar. It's not intended to be a replacement
for the calendar you already use.

## Example of use

```
$ python generate-calendar.py events.txt 2018-7-2 html
```

## Inputs

The file you give to it as input has a specific syntax to follow. Here is an
example of such a file:

```
# Format -- Day of week, week number, Label, repeat every, category

# This will repeat on monday, every month, starting the first week.
lun, 1, allday, Brew a new batch of beer, 1m, beer
# Add hops 3 weeks later!
lun, 3, 9h-12h, Add hops, 4w, beer
```

## Outputs

The tool is able to either:

- generate a calendar as set of HTML files, 
- generate a number of ics calendars.

![/capture.png?raw=true](/capture.png?raw=true)
