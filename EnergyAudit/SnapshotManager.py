import os
import re
from DeviceSnapshot import RSDeviceSnapshot
from DeviceSnapshot import EnergyAuditComponent
from DeviceSnapshot import EAMeasurement

class SnapshotManager(object):
    """Base class for all snapshot managers"""
    def __init__(self,profile):
        #Can call from subclass with
        #super().__init__()
        self.profile = profile
        self.devices = []
        
    #Add any interface functions
    def set_parser():
        #Default behavior
        raise NotImplementedExceptionError("Subclass not setting parser")

class RancidSnapshotManager(SnapshotManager):
    """Rancid snapshot manager"""
    #def __init__(self,profile):
    # if needed
    #    super(RancidSnapshotManager,self).__init__(profile)
    
    def __init__(self,profile):
        if profile == "":
            return
        self.profile = profile
        self.device_paths = profile.repo_location
        self.devices = []
        self.get_device_config_paths()
        self.device_snapshots = []

    #def __init__(self):
    #    self.profile = ""
        
    def get_snapshot_single(self, filename ):
        #No profile exists so don't store
        #Get device snapshot
        return self.run_rancid_parser(filename)

    def take_dev_snapshot(self):
        for d in self.devices:
            self.device_snapshots.append(self.run_rancid_parser(d))

    def take_doit_snapshot(self):
        print "Loading dev mapping"
        doit_dev_type = open('/home/jpchaba/repo/project/EnergyAudit/configs/doit/doit_no_oid.dat','r')
        dd_type = {}
        for lines in doit_dev_type:
            toks = lines.rstrip().split()
            if len(toks) != 2:
                print "Error 38742"
                exit
            dd_type[toks[0]] = toks[1]

        oid_dat= open('/home/jpchaba/repo/project/EnergyAudit/oid2cli.dat','r')
        oid2cli = {}
        for lines in oid_dat:
            toks = lines.rstrip().split()
            if len(toks) != 2:
                print "Error 38742"
                exit
            print toks
            oid2cli[toks[0]] = toks[1]      
        
        print "Parsing devices"
        for d in self.devices:
            self.device_snapshots.append(self.run_doit_parser(d,dd_type,oid2cli))
        
    def run_rancid_parser(self, config_path):
        #Refactor dev_snapshot it is being passed
        #and saved as a class member, duplication
        dev_snapshot = RSDeviceSnapshot()
        rancid_parser = RancidConfigParser(config_path, "switch",dev_snapshot)    
        rancid_parser.run_parser(dev_snapshot)
        return dev_snapshot

    def run_doit_parser(self, config_path, dd_type, oid2cli):
        #Get configuration device type
        # strip off trailing .conf match to dd_type
        dev_t = (config_path.split('/')[-1])[:-5]
        if dev_t not in dd_type:
            #No configuration file for device
            #print dev_t
            #print "Unknown device !!!!BAD"
            return
        # JPC: Considering stacked switches
        # as components

        #[JPC]Pull in file that maps oid2cli
        dev_snapshot = RSDeviceSnapshot()
        dev_snapshot.dev_manufacturer = "cisco"
        nameIT = ""
        if dd_type[dev_t] in oid2cli:
            nameIT = oid2cli[dd_type[dev_t]]
        else:
            nameIT = dd_type[dev_t]
        dev_snapshot.chassis_type = nameIT
        #print "Parse: "+config_path+ ":" +str(dev_t)+":"+str(dd_type[dev_t])
        doit_parser = RancidConfigParser(config_path,"switch",dev_snapshot)
        doit_parser.run_parser(dev_snapshot)
        return dev_snapshot 
        
    def add_device_path(self, dir_path, dev_type):
        self.device_paths.append(dir_path)
        self.device_paths.append(dev_type)

    def get_device_config_paths(self):
        for repo_location in self.device_paths:
            if repo_location[0] == '#':
                return []
            repo_list = self.get_repo_listing(repo_location)
            self.devices.extend(repo_list)
        
    def print_device_paths(self):
        print "Device paths:"
        for entries in self.device_paths:
            print entries

    def print_config_files(self):
        print "Devices under test:"
        for entries in self.devices:
            print "CONFIG: "+entries

    def get_repo_listing(self,dev_path):
        retVal = []
        for filename in os.listdir(dev_path):
            if filename != "CVS": 
                retVal.append(dev_path+"/"+filename)
        return retVal

    def print_all_snapshots(self):
        for d in self.device_snapshots:
            d.print_dev_snapshot()

#Refactor to put all of this in the right place
#Currently using the flat file version of the database
#use EADeviceAdd:convert_file_database to create sql version
    def run_audit_file(self, filename):
        # Pull in comparative snapshots
        print "Run Audit"
        pwr_m = []
        fsnap = open('snap.dat', 'r')
        print "Loading measurements"
        for line in fsnap:
            eam = EAMeasurement()
            eam.parse_measurement(line)
            pwr_m.append(eam)
        print "Done loading"
        # Match snapshots in community database to those seen
        # by the parser
        no_match = []
        nm_num  = 0
        pwr_consumption = 0.0
        num_devices = 0
        names_count = {}
        power_pie = {}
        no_chassis_type = 0
        for d in self.device_snapshots:
            num_devices = num_devices+1
            #print d.chassis_type
            ppc = 0.0
            if not d or d.chassis_type == "":
                no_chassis_type = no_chassis_type+1
                continue
            if not d.is_stack_switch:
                if d.chassis_type.lower() in names_count:
                    names_count[d.chassis_type.lower()] =  names_count[d.chassis_type.lower()]+1
                else:
                    names_count[d.chassis_type.lower()] = 1
            nm = True
            if d.is_stack_switch:
                num_devices = num_devices-1
                for c in d.components:
                    if c.type == "stack":
                        num_devices = num_devices+1
                        if c.name.lower() in names_count:
                            names_count[c.name.lower()] =  names_count[c.name.lower()]+1
                        else:
                            names_count[c.name.lower()] = 1
                        #Check the measured devices
                        nm = True
                        for m in pwr_m:
                            if(m.snapshot.dev_comp_match(c)):
                                pwr_consumption = pwr_consumption+m.power_measurement
                                if c.name.lower() in power_pie:
                                    power_pie[c.name.lower()] =  power_pie[c.name.lower()]+m.power_measurement
                                else:
                                    power_pie[c.name.lower()] = m.power_measurement
                                nm = False
                                for m_comp in m.snapshot.components:
                                    if m_comp.name == "ppcost":
                                        ppc = m_comp.power
                                        break
                                break
                        if nm:
                            nm_num = nm_num+1
                            if c.name not in no_match:
                                no_match.append(c.name)            
            #[JPC]: multiple measurements from the same device currently will result in pathological behavior
            nm = True
            for m in pwr_m:
                if d.dev_match(m.snapshot):
                    if not d.is_stack_switch: #Already added chassis costs
                        pwr_consumption = pwr_consumption + m.power_measurement
                        if d.chassis_type.lower() in power_pie:
                            power_pie[d.chassis_type.lower()] =  power_pie[d.chassis_type.lower()]+m.power_measurement
                        else:
                            power_pie[d.chassis_type.lower()] = m.power_measurement
                        
                    #Check for components
                    # d is the test snapshot
                    # m is the measured snapshot
                    # Find per port cost
                    for m_comp in m.snapshot.components:
                        if m_comp.name == "ppcost":
                            ppc = m_comp.power
                            break
                    # No per port cost
                    if ppc == 0.0:
                        nm = False
                        break
                    # Add per port costs to overall power cost
                   
                    for tc in d.components:
                        if "thernet" in tc.name or "thernet" in tc.type or "thernet" in tc.desc:
                            pwr_consumption = pwr_consumption + ppc
                            if d.chassis_type.lower() in power_pie:
                                power_pie[d.chassis_type.lower()] =  power_pie[d.chassis_type.lower()]+ppc
                            else:
                                power_pie[d.chassis_type.lower()] = ppc
                            
                    nm = False
                    break
            if nm:
                if d.is_stack_switch == False:
                    nm_num = nm_num+1
                if d.chassis_type not in no_match:
                    no_match.append(d.chassis_type)

        #[JPC] Separate the print from the Audit function
        
        
        blarg = 0
        for k,v in names_count.iteritems():
            blarg = blarg+1
            print k,v
        print "---"
        for k1,v1 in power_pie.iteritems():
            print k1,v1
        print "---"
        print "Type of devices: "+str(blarg)

        #for i in no_match:
        #    print i
        print "Type Count: "+str(blarg)
        print str(len(no_match))+" Device types without a match:"
        print str(nm_num)+" Devices without a match:"
        print "Length of device array:"+str(len(self.device_snapshots))
        print "Audit Num Devices: "+str(num_devices)
        print "Audit Power Consumption: "+str(pwr_consumption)
        print "No Chassis Type: "+str(no_chassis_type)

            

#class ConfigParser(object):

class RancidConfigParser:#(ConfigParser):
    def __init__(self,config_path, dev_type, dev_snapshot):
        self.config_path = config_path
        self.dev_type = dev_type
        self.dev_snapshot = dev_snapshot
        try:
            self.config_read = open(self.config_path,'r')
        except IOError:
            print "Cannot open device config file: "+self.config_path
        self.valid_types = {}
        self.set_switch()

    def set_switch(self):
        self.valid_types["!Chassis"] = self.dev_snapshot.m_set_chassis_type
        self.valid_types["!RANCID-CONTENT-TYPE:"] = self.dev_snapshot.m_set_dev_manufacturer
    
    def line_parser(self,line,dev_snapshot):
       # print "begin line parser"
        tokens = line.split()
        #Single line
        if tokens[0] in self.valid_types:
            #print "valid types"
            self.valid_types[tokens[0]](tokens)
        #Multiple line
        if re.match("!Slot \d+:", line):
            #New slot found
            #print "slot"
            line2 = self.config_read.readline().rstrip()
            line3 = self.config_read.readline().rstrip()
            self.set_slot(line, line2, line3, dev_snapshot)
        if re.match("interface ",line):
            #get rest of block
            #print "interface"
            new_line = self.config_read.readline().rstrip()
            block = line+"\n"
            too_long = 0
            while not re.match(r'!',new_line):
                block = block+new_line+"\n"
                new_line = self.config_read.readline().rstrip()
                too_long = too_long+1
                if too_long == 100:
                    break
            self.set_interface_port(block,dev_snapshot)
        if re.match("switch \d+ provision",line):
            dev_snapshot.is_stack_switch = True
            #print "begin set stack switch"
            self.set_stack_switch(line, dev_snapshot)
            #print "end set stack switch"
       # print "done line parser"
                

#Still need to implement stackable switches
#   def set_stackable(self,name_block)

    def set_stack_switch(self, line, dev_snapshot):
        d_name = (line.rstrip().split())[-1]
        c = EnergyAuditComponent()
        c.set_name(d_name)
        c.set_status("up")
        c.type = "stack"
        c.position = int((line.rstrip().split())[1])
        dev_snapshot.add_component(c)
        
        
    def set_interface_port(self, interface_block,dev_snapshot):
        comp_type = "interface_port"
        name = re.match( r'interface (\S+)', interface_block).group(1)
        status = "on"
        desc = re.match( r'interface (\D+)\d', interface_block).group(1)
        if re.search( r'shutdown\n', interface_block):
            status = "off"
        position = re.match( r'interface [\w-]+(\d+\S*)', interface_block).group(1)
        if "Vlan" in name or "Loopback" in name:
            return
        else:
            c = EnergyAuditComponent(comp_type, name, desc, status, 1, position,"")
        dev_snapshot.add_component(c)
        #What to do with vlan loopback port channel etc.
        

    def set_slot(self, l_type, l_part, l_vers,dev_snapshot):
        #CISCO 2921 is not in this format so slot parser
        #needs to be expanded to be more flexible
        #ATM FT I'm just going to swallow exceptions
        try:
            ports = re.search( r'(\d+) ports', l_type ).group(1)
            name = re.search( r'part (\S+),', l_part ).group(1)
            desc = re.search( 'type (\S+)', l_type ).group(1)
            vers = re.search( 'hvers (\S+)', l_vers ).group(1)
            status = "on" 
            position = re.search( r'!Slot (\d+):', l_type ).group(1)
            comp_type = "Router Linecard"
            c = EnergyAuditComponent(comp_type,name,desc,status,ports,position,vers)
            dev_snapshot.add_component(c)
        except:
            pass 

    def run_parser(self, dev_snapshot):
        #return list of
        line = self.config_read.readline().rstrip()
        while line:
            self.line_parser(line,dev_snapshot)
            line = self.config_read.readline().rstrip()
            

        
        
