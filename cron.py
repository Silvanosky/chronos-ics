#! /usr/bin/env python3

import os
import datetime
import concurrent.futures
import time

import jinja2

import chronos

STUDENT_PROM = 2020
ASSISTANT_PROM = STUDENT_PROM - 2
OUTPUT = 'build'
CALDIR = os.path.join(OUTPUT, 'calendars')
NUMWEEKS = 80

GROUPS = ["INFOS1A1-1", "INFOS1A1-2", "INFOS1A2-1", "INFOS1A2-2", "INFOS1B1-1", "INFOS1B1-2",
          "INFOS1B2-1",
          "INFOS1B2-2",
          "INFOS1C1-1",
          "INFOS1C1-2",
          "INFOS1C2-1",
          "INFOS1C2-2",
          "INFOS1D1-1",
          "INFOS1D1-2",
          "INFOS1D2-1",
          "INFOS1D2-2",
          "INFOS1E1-1",
          "INFOS1E1-2",
          "INFOS1E2-1",
          "INFOS1E2-2",
          "INFOS1INT1-1",
          "INFOS1INT2-2",
          "INFOS1INT2-1",
          "INFOS1INT2-2",
          ]

def get_calendar(promo, group):
    output = '{}/{}'.format(CALDIR, group)
    cal = chronos.chronos(promo, group, NUMWEEKS)
    print("ecriture: " + output)
    with open('{}.ics'.format(output), 'wb') as out:
        out.write(cal.to_ical())

def update_index():
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
    template = env.get_template('index.html')

    groups = [
        {'title': 'Groups', 'cals': GROUPS},
    ]
    for group in groups:
        group['cals'] = map(lambda x: (x, time.ctime(
            os.path.getmtime('{}/{}.ics'.format(CALDIR, x)))), group['cals'])

    output = template.render(groups=groups)
    with open(os.path.join(OUTPUT, "index.html"), "w") as f:
        f.write(output)


if __name__ == '__main__':
    for d in [OUTPUT, CALDIR]:
        if not os.path.isdir(d):
            os.mkdir(d)

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        for i in GROUPS:
            executor.submit(get_calendar, STUDENT_PROM, i)

    update_index()
