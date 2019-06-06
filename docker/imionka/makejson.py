import random

with open("imionka.txt", "r") as f:
    imionka = f.readlines()
    for i in range(len(imionka)):
        imionka[i] = imionka[i].strip()

with open("nazwiska.txt", "r") as f:
    nazwiska = f.readlines()
    for n in range(len(nazwiska)):
        nazwiska[n] = nazwiska[n].strip()

random.shuffle(imionka)
imionka = imionka[:400]
random.shuffle(nazwiska)
nazwiska = nazwiska[:400]

with open("powody.txt", "r") as f:
    powody = f.readlines()
    for p in range(len(powody)):
        powody[p] = powody[p].strip()

powo = powody

with open("stanowiska.txt", "r") as f:
    stan = f.readlines()
    for s in range(len(stan)):
        stan[s] = stan[s].strip()

with open("michaltopedal.txt", "r") as f:
    upr = f.readlines()
    for u in range(len(upr)):
        upr[u] = upr[u].strip()

import json
import copy

with open("stan.json", "r") as f:
    stans = json.load(f)

stans_id = {}
for key, val in stans.items():
    stans_id[key] = []
    for elem in val:
        stans_id[key].append(upr.index(elem) + 1)

final = []


permission = {
    "model": "app.permission",
    "pk": 0,
    "fields": {
        "name": "Administracja"
    }
}

list_perms = []

for up in upr:
    permission["pk"] += 1
    perm = copy.deepcopy(permission)
    perm['fields']['name'] = up
    final.append(perm)    

pos = {
    "model": "app.position",
    "pk": 0,
    "fields": {
        "name": "Aaa",
        "permissions": []
    }
}

list_pos = 0

for po in stan:
    pos["pk"] += 1
    sta = copy.deepcopy(pos)
    sta['fields']['name'] = po
    sta['fields']['permissions'] = stans_id[po]
    final.append(sta)
    list_pos += 1

sub = {
    "model": "app.substitutionreason",
    "pk": 0,
    "fields": {
        "desc": "aaa"
    }
}

list_sub = []

for su in powo:
    sub["pk"] += 1
    subb = copy.deepcopy(sub)
    subb['fields']['desc'] = su
    final.append(subb)

permch = {
    "model": "app.permissionchangereason",
    "pk": 1,
    "fields": {
        "desc": "zwolnienie"
    }
}

list_permch = []
permch2 = copy.deepcopy(permch)
permch2['pk'] += 1
permch2['desc'] = "awans"
final.append(permch)
final.append(permch2)

worker = {
  "model": "app.worker",
  "pk": 0,
  "fields": {
    "supervisor": 1,
    "name": "Test",
    "surname": "Test",
    "salary": 11111,
    "position": 2,
    "employment_date": "2019-05-08"
  }
}

list_worker = []

import time

def strTimeProp(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def randomDate(start, end, prop):
    return strTimeProp(start, end, '%Y-%m-%d', prop)

for i in range(len(imionka)):
    worker['pk'] += 1
    work = copy.deepcopy(worker)
    work['fields']['supervisor'] = random.randint(1,4)
    work['fields']['name'] = imionka[i]
    work['fields']['surname'] = nazwiska[i]
    work['fields']['salary'] = random.randint(18, 200) * 100
    work['fields']['position'] = random.randint(1, list_pos)
    work['fields']['employment_date'] = randomDate("2015-01-01", "2019-01-01", random.random())
    final.append(work)

with open("out.json", "w") as f:

    json.dump(final, f)
    


