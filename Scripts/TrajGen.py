import os
import csv

import mysql.connector

javapath = "../out/artifacts/TrajGen_jar/trajGen.jar"
os.environ['CLASSPATH'] = javapath

from jnius import autoclass

count = 0
countuser = 0
conn = mysql.connector.connect(host='localhost', user='root', passwd='symwrm', db='geolife', port=3306)
for rt, dirs, files in os.walk('../RawGeoLife'):
    if not files:
        continue
    countuser += 1
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS `rawtraj`;')
    cur.execute('CREATE TABLE `rawtraj` (`id` mediumint(8) NOT NULL AUTO_INCREMENT,`lat` varchar(255)' +
                ' DEFAULT NULL,`lon` varchar(255) DEFAULT NULL,`timestamp` datetime DEFAULT NULL,' +
                'PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8;')
    cur.close()
    conn.commit()

    for fname in files:
        count += 1
        print "file" + str(count) + "importing"
        filein = open(rt+'/'+fname)
        flag = False
        datas = []

        for line in filein.readlines():
            line = line.strip()
            if line == "0":
                flag = True
                continue
            if not flag:
                continue
            parts = line.split(',')
            datas.append((float(parts[0]), float(parts[1]), parts[5]+' '+parts[6]))

        cur = conn.cursor()
        cur.executemany('insert into rawtraj(lat,lon,timestamp) values(%s,%s,%s)', datas)
        cur.close()
        conn.commit()

    PyInterface = autoclass('trajGen.analysis.PyInterface')
    PyInterface.getTrace(300, 0.4, 30)
    cur = conn.cursor()
    cur.execute("show tables like 'user000%'")
    tables = cur.fetchall()
    cur.close()
    for table in tables:
        userno = table[0].replace('user000', 'user'+str(countuser))
        print("write "+userno)
        cur = conn.cursor()
        cur.execute('select * from '+table[0])
        fileo = open('../TrajData/GeoLife/'+userno+'.csv', 'wb')
        writer = csv.writer(fileo)
        entries = cur.fetchall()
        writer.writerows(entries)
        fileo.close()
        cur.execute('drop table '+table[0])
        cur.close()
        conn.commit()
conn.close()