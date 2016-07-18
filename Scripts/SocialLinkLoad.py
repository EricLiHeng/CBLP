import csv
import itertools
from operator import itemgetter

import mysql.connector

conn = mysql.connector.connect(host='localhost', user='root', passwd='symwrm', db='sociallink', port=3306)
cur = conn.cursor()
cur.execute('select * from timeline_whu_changed')
raw = cur.fetchall()
groups = itertools.groupby(raw, itemgetter(0))
count = 0
for name, traj in groups:
    count += 1
    traj = list(traj)
    length = len(traj)
    if length < 30:
        continue
    print count
    sequence = itertools.izip(range(length), [item[2] for item in traj], [item[2] for item in traj],
                              [long(item[1])*1000 for item in traj])
    fileo = open('../TrajData/SocialLink/userSL_0_0_'+str(count)+'_'+str(length)+'.csv', 'wb')
    writer = csv.writer(fileo)
    writer.writerows(sequence)
    fileo.close()