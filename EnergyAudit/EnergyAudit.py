#!/usr/bin/env python

import sys

from EnergyAuditProfile import EnergyAuditProfile
from SnapshotManager import RancidSnapshotManager



profile = EnergyAuditProfile()
profile.open_profile()
snapshots = RancidSnapshotManager(profile)

#This is for normal rancid
if len(sys.argv) == 1:
    snapshots.take_dev_snapshot()
    snapshots.run_audit_file("snap.dat")
else:
    print "DOIT Snapshot"
    snapshots.take_doit_snapshot()
    print "snapshots complete"
    snapshots.run_audit_file("snap.dat")
