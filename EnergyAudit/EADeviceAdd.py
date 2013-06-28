#!/usr/bin/env python

from EnergyAuditProfile import EnergyAuditProfile
from SnapshotManager import RancidSnapshotManager
from DatabaseManager import EADatabase
from DeviceSnapshot import EAMeasurement

import sys

#if len(sys.argv) != 4:
#    print "Incorrect number of parameters"
#    print "Usage: ./EADeviceAdd.py file|databse|simple| name value"
#    print "if: simple usage is ./EADeviceAdd.py simple| <dev_manufacturer:chassis_type:[component_name:component_power]*> value"
#    exit(1)

#[JPC] Should remove and use mysql AUTO_INCREMENT Instead
last_id = -255
try:
    fread = open('.insert_id', 'r')
    last_id = int(fread.readline().rstrip())
    fread.close()
except:
    #[JPC] Needs error checking
    last_id = 0

#Database add
def database_add():
#[JPC] refactor routine
    ed = EADatabase()
    ed.simple_db_test()

    snapshot = RancidSnapshotManager()

    dev_snap = snapshot.get_snapshot_single(sys.argv[2])
    ed.insert_dev_file(last_id, dev_snap, sys.argv[3])

def convert_file_database(last_id):
    ea_read = open('snap.dat','r')
    ed = EADatabase()
    ed.simple_db_test()
    ed.simple_db_test()
    for line in ea_read:
        eam = EAMeasurement()
        eam.parse_measurement(line)
        ed.ins_device_sql(last_id, eam.snapshot.dev_manufacturer, eam.snapshot.chassis_type, eam.power_measurement)
        for comp in eam.snapshot.components:
            ed.ins_component_sql(last_id,comp)
        last_id = last_id+1
            

def file_add():
#File add
    ea_write = open('snap.dat','a')
    em = EAMeasurement()
#ed.simple_db_test()

    snapshot = RancidSnapshotManager("")
    dev_snap = snapshot.get_snapshot_single(sys.argv[2])
    em.write_measurement(ea_write, dev_snap, sys.argv[3])
    ea_write.close()

def simple_add():
    ea_write = open('snap.dat','a')
    em = EAMeasurement()
    em.write_simple_measurement(ea_write, sys.argv[2], sys.argv[3])
    ea_write.close()

if "database" in sys.argv[1]:
    database_add()
elif "file" in sys.argv[1]:
    file_add()
elif "simple" in sys.argv[1]:
    simple_add()
elif "convert" in sys.argv[1]:
    convert_file_database(last_id)
else:
    print "Incorrect usage: "+ sys.argv[1] + " use one of file|databse|simple instead"

fwrite = open('.insert_id','w')
fwrite.write(str(last_id+1)+"\n")
fwrite.close()
