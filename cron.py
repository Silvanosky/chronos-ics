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
NUMWEEKSEND = 130
NUMWEEKSSTART = 105

GROUPS = ["INFOS3A1-1", "INFOS3A1-2",
          "INFOS3A2-1", "INFOS3A2-2",
          "INFOS3B1-1", "INFOS3B1-2",
          "INFOS3B2-1", "INFOS3B2-2",
          "INFOS3C1-1", "INFOS3C1-2",
          "INFOS3C2-1", "INFOS3C2-2",
          "INFOS1B2-2"
         ]
         
def gen_Groups():
    semesters = []
    for semester in range(1,5):
        r = []
        for letter in ["A", "B", "C", "D", "E"]:
            for sub in range(1,3):
                for english in range(1, 3):
                    r.append("INFOS" + str(semester) + str(letter) + str(sub) + "-" + str(english))
        semesters.append(r)
    return semesters

def get_calendar(promo, group):
    output = '{}/{}.ics'.format(CALDIR, group)
    cal = chronos.chronos(promo, group, NUMWEEKSSTART, NUMWEEKSEND)
    print("ecriture: " + output)
    with open('{}'.format(output), 'w') as out:
        out.writelines(cal)

def update_index(data):
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
    template = env.get_template('index.html')

    groups = []
    for i in range(1, 5):
        groups.append({'title': 'S'+str(i), 'cals': data[i-1]})

    for group in groups:
        cal = []
        for name in group['cals']:
            if os.path.isfile('{}/{}.ics'.format(CALDIR, name)):
                cal.append((name, time.ctime(os.path.getmtime('{}/{}.ics'.format(CALDIR, name)))))
        group['cals'] = cal
        
    output = template.render(groups=groups)
    with open(os.path.join(OUTPUT, "index.html"), "w") as f:
        f.write(output)


if __name__ == '__main__':
    for d in [OUTPUT, CALDIR]:
        if not os.path.isdir(d):
            os.mkdir(d)
    data = gen_Groups()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=60) as executor:
        for j in data:
            for i in j:
                executor.submit(get_calendar, STUDENT_PROM, i)

    update_index(data)
