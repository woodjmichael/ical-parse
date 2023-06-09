Given a downloaded google calendar in .ical format, read and parse the events based on start, end,
duration, and some parsing of the summary into 'project' and 'task'.

# Requirements
_As tested, will likely work with other versions and OSs_
- python 3.8
- pandas 2.0.1
- Ubuntu 22.04

# Quickstart
1. Download a google calendar as .ics
2. Run
```bash
python ical_parse.py -f your_filename.ics
```
