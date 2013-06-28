
#There are two types of devices, switches
#and routers, need to decide whether to implement
#seperate parsers, classes,etc. or just hack together
class DeviceSnapshot(object):
    """Base class for EnergyAudit device types"""
    def __init__(self):
        self.components = []
    def set_comment(self, comment):
        self.comment = comment
    def add_component(self, c):
        self.components.append(c)

class EAMeasurement:
    def __init__(self):
        self.snapshot = RSDeviceSnapshot()
        self.power_measurement = 0.0

    def parse_measurement(self, line):
        toks = line.split(':')
        self.snapshot.dev_manufacturer = toks[0]
        self.snapshot.chassis_type = toks[1]
        self.power_measurement = float(toks[2])
        for i in range(3,len(toks),2):
            eac = EnergyAuditComponent()
            eac.add_simple_comp(toks[i],toks[i+1])
            self.snapshot.components.append(eac)

    def write_measurement(self, ea_write, snap, measurement):
        ea_write.write(str(snap.dev_manufacturer)+':'+str(snap.chassis_type)+':'+str(measurement))
        for c in snap.components:
            ea_write.write(":"+str(c.name)+":"+str(c.power))
        ea_write.write("\n")

    def write_simple_measurement(self, ea_write, cmd2 = "", cmd3 = ""):
        #There are a couple of different implementations for this
        #currently picking a compound string in cmd2 followed
        #by a float measurmement.
        print "Adding " +cmd2+ " to snap file"
        toks = cmd2.rstrip().split(':')
        if len(toks) < 2:
            print "incorrect simple measurment argument: <dev_manufacturer:chassis_type"
        #if len(toks) % 2 != 0:
        #    print "odd number of arguments: try again"
        dev_type = toks[0]
        chassis_type = toks[1]
        try:
            measurement_value = float(cmd3)
        except: 
            print "invalid measurmement value type"
            print cmd3
        ea_write.write(str(dev_type)+':'+str(chassis_type)+':'+str(measurement_value))
        if len(toks)==3:
            ea_write.write("\n")
            return
        for i in range(3,len(toks),2):
            pwr = 0.0
            try:
                pwr = float(toks[i+1])
            except: 
                print "invalid measurmement value type"
                print toks[i+1]
            ea_write.write(":"+toks[i]+":"+str(pwr))
        ea_write.write("\n")
        
                    
#Entire switches can now be switch components
#thanks to stackable swtiches
class EnergyAuditComponent:
    def eq_name(self, comp):
        if self.name == comp.name:
            return True
        return False

    def add_simple_comp(self, name, power):
        self.name = name
        try:
            self.power = float(power)
        except: #Value type or something
            print "Invalid measurement value"
            print toks[i+1]

    def __init__(self,t="", name="", desc="", status="", ports="",pos="",ver=""):
        self.type = t
        self.name = name
        self.desc = desc
        self.status = status
        self.ports = ports
        self.position = pos
        self.version = ver
        self.power = 0 #Default is whole device measurement

    def set_power(self,p):
        self.power = p
    def set_name(self, n):
        self.name = n
    def set_desc(self, d):
        self.desc = d
    def set_status(self, s):
        self.status = s
    def set_ports(self,p):
        self.ports = p
    def print_component(self):
        print "\t\t"+str(self.type)+":"+str(self.name)+":"+str(self.desc)+":"+str(self.status)+":"+str(self.ports)+":"+str(self.position)+":"+str(self.version)

class RSDeviceSnapshot(DeviceSnapshot):
    def __init__(self):
        self.dev_manufacturer = ""
        self.chassis_type = ""
        self.is_stack_switch = False
        self.components = []
        

    def eq_dev_name(self, comp):
        if self.chassis_type == comp.chassis_type or str(self.chassis_type).lower() == str(comp.chassis_type).lower():
            return True
        return False

    def m_set_chassis_type(self,ctype):
        self.chassis_type = ctype[2]

    def m_set_dev_manufacturer(self,dtype):
        self.dev_manufacturer = dtype[1]

#[JPC] add aliasing match here
    def dev_match(self, rs_dev):
        if self.eq_dev_name(rs_dev):
            return True
        return False

    def dev_comp_match(self, comp):
        if str(self.chassis_type).lower() == str(comp.name.lower()):
            return True
        return False
        
    def print_dev_snapshot(self):
        print
        print "Manufacturer: "+ self.dev_manufacturer
        print "Chassis Type: "+ self.chassis_type
        print
        for c in self.components:
            c.print_component()

