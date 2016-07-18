
import mysql.connector

def loadtrace(filein):


    datas = []
    for line in filein.readlines():
        parts = line.split(',')
        datas.append((round(float(parts[1]), 2), round(float(parts[2]), 2)))

    try:
        conn = mysql.connector.connect(host='localhost', user='root', passwd='symwrm', db='geolife', port=3306)
        cur = conn.cursor()
        cur.execute('DROP TABLE IF EXISTS `traj`;')
        cur.execute('CREATE TABLE `traj` (`id` mediumint(8) NOT NULL AUTO_INCREMENT,`lat` varchar(255)' +
                    ' DEFAULT NULL,`lon` varchar(255) DEFAULT NULL,' +
                    'PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8;')
        cur.execute('DROP TABLE IF EXISTS `predict`;')
        cur.execute('CREATE TABLE `predict` (`id` mediumint(8) NOT NULL AUTO_INCREMENT,`lat` varchar(255)' +
                    ' DEFAULT NULL,`lon` varchar(255) DEFAULT NULL,' +
                    'PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8;')
        cur.executemany('insert into traj(lat,lon) values(%s,%s)', datas)

        cur.close()
        conn.commit()
        conn.close()
    except mysql.connector.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def refresh():
    try:
        conn = mysql.connector.connect(host='localhost', user='root', passwd='symwrm', db='geolife', port=3306)
        cur = conn.cursor()
        cur.execute('DROP TABLE IF EXISTS `predict`;')
        cur.execute('CREATE TABLE `predict` (`id` mediumint(8) NOT NULL AUTO_INCREMENT,`lat` varchar(255)' +
                    ' DEFAULT NULL,`lon` varchar(255) DEFAULT NULL,' +
                    'PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8;')
    except mysql.connector.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])