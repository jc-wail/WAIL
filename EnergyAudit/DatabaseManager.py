#!/usr/bin/env python

import mysql.connector
from DeviceSnapshot import RSDeviceSnapshot
from DeviceSnapshot import EnergyAuditComponent

config = {
  'user': 'EnergyAudit',
  'password': 'energyaudit',
  'host': 'localhost',
  'database': 'energyaudit',
  'raise_on_warnings': True,
}

class EADatabase:
    """Requires mysql connector and ea database setup"""
    
    def __init__(self):
        #By default connect to default setup
        self.cnx = ""
        try:
            #print "Opened Mysql database"
            self.cnx = mysql.connector.connect(**config)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong your username or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            #self.cnx.close()
            print "Connected to database"
    
#Not sure about python stuff, do I need a del?    
#    def __del__(self):
#        try:
#            self.cnx.close()
#        except:
#            print "Problem closing db, maybe never created"

    def simple_db_test(self):
        try:
            cmd = "select user(), current_date;"
            cursor = self.cnx.cursor()
            cursor.execute(cmd)
            for line in cursor:
                print line
            cursor.close()
        except mysql.connector.Error as err:
            print("Failed simple db cursor execute: {}".format(err))
            exit(1)

    def ins_device_sql(self, d_id, manufacturer, dev_type, snap):
        """Create device sql insertion string from devsnapshot"""
        print "Insert device"
        try:
            c = self.cnx.cursor()
            ins_string = "INSERT INTO EADevice (DID, DevManufacturer, DevType, Snap)  VALUES ("+str(d_id)+",\""+str(manufacturer)+"\",\""+str(dev_type)+"\","+str(snap)+");"
        #c.execute("""INSERT INTO EADevice (DID, DevManufacturer, DevType, Snap)
        #             VALUES (%s, %s, %s,%s)""", (d_id, manufacturer, dev_type, snap))
        #for line in c:
        #    print line
        #print ins_string
            c.execute(ins_string)
            c.close()
        except mysql.connector.Error as err:
            print("Failed simple db cursor execute: {}".format(err))
            exit(1)
        self.cnx.commit()


    def ins_component_sql(self, d_id, comp):
        """Create component sql insertion string from devsnapshot"""
        print "---Insert component"
        c = self.cnx.cursor()
        c.execute("""INSERT INTO EAComp (DID, Type, Name, Description, Status, Ports, Position, Version, Snap)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""", (d_id, comp.type, comp.name, comp.desc, comp.status, comp.ports, comp.position, comp.version, comp.power))
        #for line in c:
        #    print line
        c.close()
        self.cnx.commit()

    def insert_dev_file(self, d_id, dev_snapshot, pwr_measurement):
        """Insert a parsed rancid snapshot with power measurement"""
        strs_to_insert = []
        strs_to_insert.extend(self.ins_device_sql(d_id,dev_snapshot))
        for c in dev_snapshot.components:
            strs_to_insert.extend(self.ins_component_sql(d_id,c))
        print 
        print "---"
        print strs_to_insert
        print pwr_measurement
        print "---"
        print


                               
