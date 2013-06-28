import os

class EnergyAuditProfile:
    """Building and maintaining the admin profile"""
    def __init__(self):
        self.config_path = os.getcwd()+"/.energy_audit"
        #Multiple repos will require object or maps or somethin
        #for type and location
        self.repo_type = ""
        self.repo_location = []

    def profile_exist(self):
        # Exploit/Thread problem: create file after check
        # Result: creator wins/interleaving
        # Fix: Lock or open file
        if os.path.exists(self.config_path) and os.path.isfile(self.config_path) and os.access(self.config_path, os.R_OK):
            #File exists
            return True
        return False

    def open_profile(self):
        if not self.profile_exist():
            self.create_profile()
        self.read_profile()

    def create_profile(self):
        try:
            config_write = open(self.config_path,'w')
            repo_type = raw_input("Enter repo type (Rancid)|SNMP: ") or 'Rancid'
            config_write.write(repo_type+"\n")
            while self.add_a_repo(config_write) == "next":
                continue
        except IOError as e:
            #Cannot open or add
            print "cannot open "+self.config_path+" file for writing"
        config_write.close()

    def add_a_repo(self, config_write):
        repo_location = raw_input("Enter repo location|(q)uit: ") or os.getcwd()+"q"
        if repo_location == "q":
            return "done"
        config_write.write(repo_location+"\n")
        return "next"
 
    def read_profile(self):
        #Read one
        try:
            profile_read = open(self.config_path,'r')
        except IOError as e:
            print "Cannot read profile: "+self.config_path
        self.repo_type = profile_read.readline().rstrip()
        print "Repository type: "+self.repo_type
        for line in profile_read:
            self.repo_location.append(line.rstrip())
            print "Repository location: "+line.rstrip()
