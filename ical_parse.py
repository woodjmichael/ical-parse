"""ical_parse.py

Given a downloaded .ical calendar format (tested for google calendar export)
save a parsed csv file with start, end, duration, and some parsing of the summary into 'project'
and 'task'
"""


import sys
import pandas as pd

if len(sys.argv)>1:
    for i,arg in enumerate(sys.argv):
        if arg == '-f':
            ics_filename = sys.argv[i+1]
            csv_filename = ics_filename.split('/')[-1].split('.')[0] + '.csv'
else:
    ics_filename = '/home/mjw/Downloads/woodjmichael@gmail.com.ical/Work - Time_5ib8d84gn65fl9e79hcmigbukc@group.calendar.google.com.ics'
    csv_filename = ics_filename.split('/')[-1].split('.')[0] + '.csv'

def find(i,key)->str:
    """_summary_

    Args:
        i (int): current index in lines of file
        key (str): key that we're looking for within a BEGIN:VEVENT

    Returns:
        str: value associated with key or 'key does not exist in this VEVENT'
    """
    for next_line in lines[i+1:i+20]:
        next_key = next_line.split(':')[0].split(';')[0]
        if next_key == key:
            return next_line.split(':')[1]
        elif next_key == 'BEGIN':
            return 'key does not exist in this VEVENT'
    return 'key does not exist in this VEVENT'

def convert_time(t)->pd.Timestamp:
    """_summary_

    Args:
        t (str): datetime

    Returns:
        pd.Datetime: datetime converted
    """
    if t != 'key does not exist in this VEVENT':
        return pd.Timestamp(t).tz_localize(None)
    else:
        return pd.Timestamp(0).tz_localize(None)
    
if __name__ == '__main__':
    with open(ics_filename,'r',encoding='UTF-8') as f:
        lines = f.readlines()

    start,end,project,task = [],[],[],[]
    for i,line in enumerate(lines):
        line = line.replace('\n','')
        if line == 'BEGIN:VEVENT':
            summary = find(i,'SUMMARY').replace('\n','').replace(',',';')
            project.append(summary.split(' - ')[0])
            if len(summary.split(' - '))>1:
                task.append(summary.split(' - ')[1])
            else:
                task.append(summary.split(' - ')[0])
            start.append(convert_time(find(i,'DTSTART').replace('\n','')))
            end.append(  convert_time(find(i,'DTEND').replace('\n','')))
            
            if summary == 'Council Meeting (FOA p2)':
                print(summary.split(' - ')[0])
                print(convert_time(find(i,'DTSTART').replace('\n','')))
                print(convert_time(find(i,'DTEND').replace('\n','')))
            
    df = pd.DataFrame({'start':start,'end':end,'project':project,'task':task})

    df['hours'] = [x.seconds/3600 for x in (df.end - df.start)]

df.to_csv(csv_filename)