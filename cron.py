#! /usr/bin/env python3

import os
import datetime
import concurrent.futures
import time

import urllib.parse

import jinja2

import chronos

STUDENT_PROM = 2020
ASSISTANT_PROM = STUDENT_PROM - 2
OUTPUT = 'build'
CALDIR = os.path.join(OUTPUT, 'calendars')
NUMWEEKS = 80

#test
GROUPS = [[], [], [], [], [], [18, 19, 22, 23]]
         
def gen_Groups():
    semesters = []
    for semester in ["1", "2", "3", "4"]:
        r = []
        for letter in ["A", "B", "C", "D", "E"]:
            for sub in range(1,4):
                for english in range(1, 3):
                    r.append("INFOS" + semester + str(letter) + str(sub) + "-" + str(english))
        semesters.append(r)
    r = []
    for group in ["A", "B", "C"]:
        for sub in range(1,3):
            r.append("GR" + group + str(sub))
    semesters.append(r)
    return semesters

def get_calendar(promo, group):
    time.sleep(0.5)
    output = '{}/{}.ics'.format(CALDIR, group)
    cal = chronos.chronos(promo, group, NUMWEEKS)
    print("ecriture: " + output)
    with open('{}'.format(output), 'w') as out:
        out.writelines(cal)

def update_index(data):
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
    template = env.get_template('index.html')

    groups = []
    i = 0;
    for g in ['S1', 'S2', 'S3', 'S4', 'ING1', 'ING2/3']:
        groups.append({'title': g, 'cals': data[i]})
        i += 1

    for group in groups:
        cal = []
        for name in group['cals']:
            if os.path.isfile('{}/{}.ics'.format(CALDIR, urllib.parse.quote_plus(str(name)))):
                path = '{}/{}.ics'.format(CALDIR, urllib.parse.quote_plus(str(name)))
                cal.append((name, urllib.parse.quote_plus(str(name)), time.ctime(os.path.getmtime(path))))
        group['cals'] = cal
        
    output = template.render(groups=groups)
    with open(os.path.join(OUTPUT, "index.html"), "w") as f:
        f.write(output)


if __name__ == '__main__':
    for d in [OUTPUT, CALDIR]:
        if not os.path.isdir(d):
            os.mkdir(d)
    data = GROUPS
    #data = gen_Groups()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        for j in data:
            for i in j:
                executor.submit(get_calendar, STUDENT_PROM, i)
        print("Done")

    update_index(data)
