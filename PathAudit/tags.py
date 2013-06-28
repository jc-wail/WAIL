#!/usr/bin/python
import sys
import re
from nose.tools import *
from pprint import pprint
import trie

#---

feature_2 = re.compile('[A-Z\-]+')
feature_5 = re.compile('[a-zA-Z][a-zA-Z]\d+')
feature_8 = re.compile('\-\d+\-\d+')

#Enum
class tag_p:
    speed,jtype,unique_ip,function,alpha,delim,geo,unknown = range(8)

class tag_bundle:
    def __init__(self):
        self.tb = []
        self.tag_dict = {}
        self.type_dict = {}
        self.tag_dict_type = {}
        
    def add_tag(self, t):
        self.tb.append(t)

    def total_tags(self):
        return len(self.tb)
        
    def gen_one_off(self):
        one_offs = open('one_offs.dat','w')
        parse_object = re.compile('[0-9]')
        #[JPC] only do this after a speed or function
        # tag.
        for i, v in self.tag_dict.iteritems():
            #Mix up name
            #For all numbers in string
            #[JPC] should implement check only if speed tag
            #for now just do it for a domain
#            bool_speed = 0
#            for tgs in v
            #Put domain check here 
            if ("speed" in self.tag_dict_type[i]) or ("function" not in self.tag_dict_type[i]):
                a = 0 #good to go
            else:
                continue
            if "ip" in self.tag_dict_type[i]:
                continue
            for m in parse_object.finditer(i):
                stride = range(1,9)
                for n in stride:                    
                    tmp = i[:m.start()]+str(int(i[m.start()])+n)+i[m.start()+1:]
                    #check that name doesn't already exist
                    if tmp not in self.tag_dict:
                        #print
                        one_offs.write(tmp)
                        one_offs.write("\n")
            # Decrement
                for n in stride:                    
                    if int(i[m.start()])-n < 0:
                        break
                    tmp = i[:m.start()]+str(int(i[m.start()])-n)+i[m.start()+1:]
                    #check that name doesn't already exist
                    if tmp not in self.tag_dict:
                        #print
                        one_offs.write(tmp)
                        one_offs.write("\n")          
            # tag diversity
            #     find similarly placed same type tags and iterate through 
            # {xe|ge|te|gi|...}
        one_offs.close()
        

#Memory inefficient, but doesn't change any objects
#in place so no
#side effects aka deleting from a dictionary iterator does what?
    def remove_overlap(self):
        #Get all tags for a specific name
        #they are already ordered by name
        tag_cat = dict()
#        print "There are %d tags in tb" %(len(self.tb))
        for tgs in self.tb:
#            print tgs.name
            if tgs.name in tag_cat:
                tag_cat[tgs.name].append(tgs)
#                print "adding to known: %d" %(len(tag_cat[tgs.name]))
            else:
                tag_cat[tgs.name] = []
                tag_cat[tgs.name].append(tgs)
#                print "New list: %d" %(len(tag_cat[tgs.name]))
#            print tag_cat
        tag_cat2 = {}
#        print "There are %d tags in the hash" %(len(tag_cat))
        #Algorithm to remove tags that overlap
        
        for k, name_tags in tag_cat.iteritems():
#            print "There are %d tags in this name" %(len(tag_cat[k]))
            v_new = []
            for v in name_tags:
                exclude = 0
#                print v.name
                for c in name_tags:
                    if ( (c.start>v.start) and (c.start<v.end) ) or ((c.end>v.start) and (c.end<v.end)) or (v.start>c.start and v.start < c.end) or (v.start<c.start and v.end>c.start):
                        v.set_tag_prio()
                        c.set_tag_prio()
                        #Remove lower priority tag
                        if v.tag_prio > c.tag_prio:
 #                           print "Remove lower priority tag"
                            exclude = 1
                        elif v.tag_prio == c.tag_prio:
#                            print "Same tag"
                            vsize = v.end-v.start
                            csize = c.end-c.start
                            if vsize < csize: #Take longer
#                                print "take longer"
                                exclude = 1
                            elif vsize==csize: #If same size
#                                print "take earlier"
                                if v.start>c.start: #Take earlier
                                    exclude = 1
                    elif c.start == v.start and c.end == v.end:
                        continue
                    else:
                        continue
                if not exclude:
                    v_new.append(v)
            tag_cat2[k] = v_new
        #Write back to list
        new_tb = []
        for k,v in tag_cat2.iteritems():
            for nametags in v:
                new_tb.append(nametags)
        self.tb = new_tb
#Remove rebuild if slow
        self.tags_per_type
        self.tags_per_name
        

    def tags_per_type(self):
        for tgs in self.tb:
            if tgs.tag_name in self.type_dict:
                self.type_dict[tgs.tag_name] =  self.type_dict[tgs.tag_name]+1
            else:
                self.type_dict[tgs.tag_name] = 1
        #print "There are %d type tags" %(len(self.type_dict))
        return self.type_dict        

    def tags_per_name(self):
        #Turn list into dictionary with ++ per entry
        for tgs in self.tb:
            if tgs.name in self.tag_dict:
                self.tag_dict[tgs.name] =  self.tag_dict[tgs.name]+1
                self.tag_dict_type[tgs.name] =  self.tag_dict_type[tgs.name]+tgs.tag_name
            else:
                self.tag_dict[tgs.name] = 1
                self.tag_dict_type[tgs.name] =  tgs.tag_name
        return self.tag_dict

    def print_tag_per_name_dis(self):
        ptpn = open('tag_per_name_dist.dat', 'w')
        itr = 1
        for k, v in self.tag_dict.iteritems():
            ptpn.write(k)
            ptpn.write(',')
            ptpn.write(str(itr))
            ptpn.write(',')
            ptpn.write(str(v))
            ptpn.write('\n')
        ptpn.close()
    
    def print_type_name_dis(self):
        type_out = open('tag_type_dist.dat', 'w')
        for k, v in self.type_dict.iteritems():
            type_out.write(k)
            type_out.write(',')
            type_out.write(',')
            type_out.write(str(v))
            type_out.write('\n')
        type_out.close() 

    def get_naming_domain(self,name):
        #JPC Tidy up later 
        t = name.split('.')
        retVal = t[-2]+"."+t[-1]
        return retVal

    def tags_per_naming_domain(self):
        ret_dict = {}
        for tgs in self.tb:
            #get naming domain
            n_domain = self.get_naming_domain(tgs.name)
            if tgs.name in ret_dict:
                ret_dict[n_domain].append(tgs)
            else:
                ret_dict[n_domain] = []
                ret_dict[n_domain].append(tgs)
        
        return ret_dict
                
    def print_top_tag_values(self):
        geo_tags = {}
        speed_tags = {}
        function_tags = {}
        alpha_num_tags = {}
        for tgs in self.tb:
            if tgs.tag_name == "geo":
                if tgs.tag_value in geo_tags:
                    geo_tags[tgs.tag_value] = geo_tags[tgs.tag_value] +1
                else:
                    geo_tags[tgs.tag_value] = 1
            elif tgs.tag_name == "function":
                spd = tgs.tag_value.split('-')
                proc_spd = re.sub('[0-9]+', '',spd[0])
                if proc_spd in function_tags:
                    function_tags[proc_spd] = function_tags[proc_spd] +1
                else:
                    function_tags[proc_spd] = 1
            elif tgs.tag_name == "speed":
                spd = tgs.tag_value.split('-')
                proc_spd = re.sub('[0-9]+', '',spd[0])
                if proc_spd in speed_tags:
                    speed_tags[proc_spd] = speed_tags[proc_spd] +1
                else:
                    speed_tags[proc_spd] = 1
            elif tgs.tag_name == "f5":
                spd = tgs.tag_value.split('-')
                proc_spd = re.sub('[0-9]+', '',spd[0])
                if proc_spd in alpha_num_tags:
                    alpha_num_tags[proc_spd] = alpha_num_tags[proc_spd] +1
                else:
                    alpha_num_tags[proc_spd] = 1
            else:
                continue

        top_geo = open('top_geo.dat', 'w')
        top_geo.write(str(len(geo_tags)))
        top_geo.write("\n\n")
        for k, v in geo_tags.iteritems():
            to_write = str(v)+"\t"+str(k)+"\n"
            top_geo.write(to_write)

        top_speed = open('top_speed.dat', 'w')
        top_speed.write(str(len(speed_tags)))
        top_speed.write("\n\n")
        for k, v in speed_tags.iteritems():
            to_write = str(v)+"\t"+str(k)+"\n"
            top_speed.write(to_write)

        top_function = open('top_function.dat', 'w')
        top_function.write(str(len(function_tags)))
        top_function.write("\n\n")
        for k, v in function_tags.iteritems():
            to_write = str(v)+"\t"+str(k)+"\n"
            top_function.write(to_write)

        top_alpha = open('top_alpha.dat', 'w')
        top_alpha.write(str(len(alpha_num_tags)))
        top_alpha.write("\n\n")
        for k, v in alpha_num_tags.iteritems():
            to_write = str(v)+"\t"+str(k)+"\n"
            top_alpha.write(to_write)
        
        top_geo.close()
        top_speed.close()
        top_function.close()
        top_alpha.close()

class j_tag:
    def __init__(self):
        self.name = ''
        self.start = 0
        self.end = 0
        self.tag_name = "tag"
        self.tag_value = "null"
        self.tag_prio = 10

    def set_tag_prio(self):
#    speed,function,jtype,alpha,geo,delim,unknown
        if self.tag_name.lower() == "speed":
            self.tag_prio = tag_p.speed
        elif self.tag_name.lower() == "unique_ip":
            self.tag_prio = tag_p.unique_ip
        elif self.tag_name.lower() == "function":
            self.tag_prio = tag_p.function
        elif self.tag_name.lower() == "type":
            self.tag_prio = tag_p.jtype
        elif self.tag_name.lower() == "f5":
            self.tag_prio = tag_p.alpha
        elif self.tag_name.lower() == "geo":
            self.tag_prio = tag_p.geo
        elif self.tag_name.lower() == "f2":
            self.tag_prio = tag_p.delim
        else:
            self.tag_prio = tag_p.unknown

    def get_tag_name(self):
        return self.tag_name
    def get_tag_value(self):
        return self.tag_value
    def get_start_pos(self):
        return self.start
    def get_end_pos(self):
        return self.end
    def set_tag_name(self,name):
        self.tag_name = name
    def set_tag_value(self,value):
        self.tag_value = value
    def set_start_pos(self,start):
        self.start = start
    def set_end_pos(self,end):
        self.end = end
    def get_whole_tag(self):
        return str(self.tag_name)+"\t"+str(self.tag_value)+"\t"+str(self.start)+"\t"+str(self.end)+"\n"
    def get_whole_tag_no_pos(self):
        return str(self.tag_name)+"\t"+str(self.tag_value)+"\n"

class MyIPAddy:
    def __init__(self):
        self.sub1 = '0'
        self.sub2 = '0'
        self.sub3 = '0'
        self.sub4 = '0'

    def add_addy( self, s1, s2, s3, s4 ):
        self.sub1 = s1
        self.sub2 = s2
        self.sub3 = s3
        self.sub4 = s4

    def return_s1( self ):
        return self.sub1
        
    def return_all( self ):
        return self.sub1+"."+self.sub2+"."+self.sub3+"."+self.sub4



#class PathSet:
#    def __init__(self):
#        self.begin = 0
#        self.end = 0
#        self.hops = []

#class HopInfo:
#    def __init__(self):

class ArkDNSEntry:
    def __init__(self):
        self.timestamp = -1
        self.ip = MyIPAddy()
        self.dns_name = '' #Refactor into own class
        self.unique_name = ''
        self.common_cisco_int = []#['fa','gi','te','pos','se','po','posch','tu','atm','vl','be','bs','tt','ti','at']
        self.common_juniper_int = []#['fe','ge','xe','so', 't1','t3','ae','as','ip-', 'gr-', 'at']
        self.gig_eth_int = []
        self.ten_gig_eth_int = []
        self.fast_eth_int = []
        self.t1 = []
        self.t3 = []
        self.link_ip = []
        self.common_core_int = []
        self.common_peering_int = []
        self.common_access_int = []
        self.letters_numbers = []
        self.build_common_cisco()
        self.build_common_juniper()
        self.build_common_core()
        self.build_common_peering()
        self.build_common_access()
        self.build_common_ten_gig()
        self.build_common_gig()
        self.build_letters_numbers()
        self.build_common_link_ip()
        self.tag_list = []

#[JPC]
    #what about deducing port, slot, (?) from pos14-0-0

    #what about per schema rules? similar to my database project ?
    #what about refining domains? template based learning
    #Temporal evolution of device names
    #Graph: tool coverage (resolve, qualities)


    def print_tags(self, outhandle):
        for t in self.tag_list:
            outhandle.write(self.dns_name+'\t'+t.get_whole_tag())

    def print_tags_console(self):
        for t in self.tag_list:
            if t.tag_name != "f2" and t.tag_name != "unique_ip":
                #print self.dns_name+'\t'+t.get_whole_tag(),
                print self.dns_name+'\t'+t.get_whole_tag_no_pos()

    def print_tags5_console(self):
        len_geo = 0
        for t in self.tag_list:
            if t.tag_name == "geo":
                if t.end-t.start > len_geo:
                    len_geo = t.end-t.start
        for t in self.tag_list:
            if t.tag_name != "f2" and t.tag_name != "unique_ip":
                if t.tag_name == "geo" and (t.end-t.start) < len_geo:
                    continue
                #print self.dns_name+'\t'+t.get_whole_tag(),
                line = t.get_whole_tag_no_pos().split('\t')
                tag_type = line[0]
                tag_value = line[1]
                ident = tag_value.split('-')[0].rstrip()
                #print self.dns_name+"\t\t"+tag_type+"\t"+ident
                if tag_type == "f5":
                    tag_type = "hint"
                print "%-42.42s\t%-12.12s\t%-12.12s" %(self.dns_name,tag_type,ident)

    def extract_tag(self, match_obj, tn, dns, offset):
        retVal = 0
        for m in match_obj.finditer(dns):
            #print "extract" 
            #print self.dns_name
            retVal=1
            t = j_tag()
            t.set_tag_name(tn)
            
            t.set_tag_value(m.group(0))
            t.set_start_pos(m.start()+offset)
            t.set_end_pos(m.end()+offset)
            self.tag_list.append(t)
            #print len(self.tag_list)
        return retVal
                
    def add_tag(self, tn, tvalue, start, end):
        t = j_tag()
        t.set_tag_name(tn)
        t.set_tag_value(tvalue)
        t.set_start_pos(start)
        t.set_end_pos(end)
        #print "extract %s,%s,%d,%d" %(tn,tvalue,start,end)
        self.tag_list.append(t)       

    def build_letters_numbers(self):
        self.letters_numbers.append(re.compile('^[a-zA-Z]+\d+$'))
        
    def build_common_link_ip(self):
        self.link_ip.append(re.compile('\d+[.]\d+[.]\d+[.]\d+'))
        self.link_ip.append(re.compile('\d+[-]\d+[-]\d+[-]\d+'))
        self.link_ip.append(re.compile('static'))
        self.link_ip.append(re.compile('\d+[.]red-\d+[-]\d+[-]\d+'))
        self.link_ip.append(re.compile('\d\d\d\d\d\d\d\d\d\d\d\d'))

    def build_common_fast_eth_int(self):
         self.fast_eth_int.append(re.compile('fa\d+-'))     
         self.fast_eth_int.append(re.compile('fe-\d+'))

    def build_t1_int(self):
        self.t1.append(re.compile('t1-\d+'))
        
    
    def build_t3_int(self):
        self.t3.append(re.compile('t3-\d+'))
        #cisco ?

    def build_common_gig(self):
        self.gig_eth_int.append(re.compile('gigabit'))
        self.gig_eth_int.append(re.compile('gibabit'))
        #what about tenge? have to run ten_gig first
        self.gig_eth_int.append(re.compile('gi\d+-'))
        self.gig_eth_int.append(re.compile('ge-\d+'))
        self.gig_eth_int.append(re.compile('gig\d+'))
        self.gig_eth_int.append(re.compile('gbe-'))

    def build_common_ten_gig(self):
        self.ten_gig_eth_int.append(re.compile('te\d*-\d+'))
        #charter
        self.ten_gig_eth_int.append(re.compile('tge\d+-'))
        self.ten_gig_eth_int.append(re.compile('tge-\d+'))
        self.ten_gig_eth_int.append(re.compile('xe\d*-\d+'))
        self.ten_gig_eth_int.append(re.compile('tenge\d+'))
        self.ten_gig_eth_int.append(re.compile('tengige\d+'))
        self.ten_gig_eth_int.append(re.compile('10gige'))
        self.ten_gig_eth_int.append(re.compile('tengige'))
        self.ten_gig_eth_int.append(re.compile('tengigabitethernet'))
        

    def build_common_cisco(self):
        #Cisco IOS
        #originally fa\d+\/\ removing \/\ requirement
        self.common_cisco_int.append(re.compile('fa\d+-'))
        self.common_cisco_int.append(re.compile('gi\d+-'))
        self.common_cisco_int.append(re.compile('te\d+-'))
        self.common_cisco_int.append(re.compile('pos\d+-'))
        self.common_cisco_int.append(re.compile('pos\d-'))
        self.common_cisco_int.append(re.compile('pos+-'))
        self.common_cisco_int.append(re.compile('pos-\d+'))
        self.common_cisco_int.append(re.compile('se\d+-'))
        self.common_cisco_int.append(re.compile('po-\d+'))
        self.common_cisco_int.append(re.compile('posch\d+'))
        self.common_cisco_int.append(re.compile('tu\d+'))
        self.common_cisco_int.append(re.compile('atm\d+-'))
        self.common_cisco_int.append(re.compile('vi\d+[^.]')) #3 digits?
        #Cisco IOS XR
        #... some already caught if need to diff put xr ios before ios
        #Too many false positives
        #self.common_cisco_int.append(re.compile('be\d+[^.]'))
        #self.common_cisco_int.append(re.compile('bs\d+[^.]'))
        #self.common_cisco_int.append(re.compile('tt\d+[^.]'))
        #self.common_cisco_int.append(re.compile('ti\d+[^.]'))
        self.common_cisco_int.append(re.compile('at\d+-[^.]'))
        #crs is a top end cisco line device
        self.common_cisco_int.append(re.compile('crs\d+[^.]'))
        
    def build_common_juniper(self):
        self.common_juniper_int.append(re.compile('fe-\d+'))
        self.common_juniper_int.append(re.compile('ge-\d+'))
        self.common_juniper_int.append(re.compile('xe\d*-\d+'))
        self.common_juniper_int.append(re.compile('so-\d+'))
        self.common_juniper_int.append(re.compile('t1-\d+'))
        self.common_juniper_int.append(re.compile('t3-\d+'))
        self.common_juniper_int.append(re.compile('ae-\d+'))
        self.common_juniper_int.append(re.compile('ae-'))
        self.common_juniper_int.append(re.compile('ae-\d'))
        self.common_juniper_int.append(re.compile('as-\d+'))
        self.common_juniper_int.append(re.compile('ip-\d+'))
        self.common_juniper_int.append(re.compile('gr-\d+'))
        self.common_juniper_int.append(re.compile('at-\d+'))
        #Not sure how \. in python re is handled following
        #is aready caught above
        #self.common_juniper_int.append(re.compile('ge-\d+-\d+-\d+\.\d+'))

    def build_common_core(self):
        #careful with false positives on two letter matches
        self.common_core_int.append(re.compile('cr\d+'))
        self.common_core_int.append(re.compile('cr\W+'))
        self.common_core_int.append(re.compile('bb\d+'))
        self.common_core_int.append(re.compile('bb\W+'))
        self.common_core_int.append(re.compile('core'))
        self.common_core_int.append(re.compile('gbr'))
        self.common_core_int.append(re.compile('ccr'))
        self.common_core_int.append(re.compile('ebr'))

    def build_common_peering(self):
        self.common_peering_int.append(re.compile('border'))
        self.common_peering_int.append(re.compile('edge'))
        self.common_peering_int.append(re.compile('peer'))
        self.common_peering_int.append(re.compile('igr'))
        self.common_peering_int.append(re.compile('br\d+'))
        self.common_peering_int.append(re.compile('br\W+'))
        self.common_peering_int.append(re.compile('ir\d+'))
        self.common_peering_int.append(re.compile('ir\W+'))

    def build_common_access(self):
        self.common_access_int.append(re.compile('aggr'))
        self.common_access_int.append(re.compile('customer'))
        self.common_access_int.append(re.compile('cust'))
        self.common_access_int.append(re.compile('hsa'))
        self.common_access_int.append(re.compile('car'))
        self.common_access_int.append(re.compile('ar\d+'))
        self.common_access_int.append(re.compile('ar\W+'))
        self.common_access_int.append(re.compile('gw\d+'))
        self.common_access_int.append(re.compile('gw\W+'))

    def add_ip(self, strs):
        fields = strs.split('.')
        if( len(fields) == 4):
            # Can pass just array for multiple args???
            self.ip.add_addy(fields[0],fields[1],fields[2],fields[3])
        else:
            print "Not enough IP fields\n"

    def get_ip(self):
        return self.ip.return_all()

    def get_dns(self):
        return self.dns_name

    def calc_unique_name(self):
        entries = self.dns_name
        #print "Unique1: %s" %(entries)
        recreate = ''
        try:
            d_name = entries.split('.')
            for i in range(0,2):
                d_name.pop()
            for parts in d_name:
                if recreate == '':
                    recreate = parts
                else:
                    recreate = recreate + "." + parts
        except:
            a = 0
        if recreate != '':
            self.unique_name = recreate
            #print "Unique2: %s" %(self.unique_name)

    def add_dns_name(self, strs):
        self.dns_name = strs
        self.calc_unique_name()

    def add_timestamp(self, strs):
        self.timestamp = strs 

    def parse_for_letters_numbers(self):
        for c in self.letters_numbers():
            if self.extract_tag(c,"lt#", self.dns_name,0):#c.findall(self.dns_name.lower()):
                return 'ln'
        return 'unknown'

    def parse_for_speed(self):
        #print "Parse for speed"
        #print self.dns_name.lower()
        for c in self.ten_gig_eth_int:
            if self.extract_tag(c,"speed",self.dns_name,0):#c.findall(self.dns_name.lower()):
                #print self.dns_name.lower()
                #print self.dns_name
                return 'xe'
        for d in self.gig_eth_int:
            if self.extract_tag(d,"speed",self.dns_name,0): # d.findall(self.dns_name.lower()):
                #print self.dns_name
                return 'ge'
        for e in self.fast_eth_int:
            if self.extract_tag(e,"speed",self.dns_name,0): #e.findall(self.dns_name.lower()):
                return 'fe'
        for f in self.t1:
            if self.extract_tag(f,"speed",self.dns_name,0): #f.findall(self.dns_name.lower()):
                return 't1'
        for g in self.t3:
            if self.extract_tag(g,"speed",self.dns_name,0): #g.findall(self.dns_name.lower()):
                return 't3'
        return 'unknown'
        
    def parse_for_int(self):
        if(self.ip.return_s1() in self.dns_name):
            #This is probably a dhcp client
            return 'client'
        else: 
            for c in self.common_cisco_int:
                if self.extract_tag(c,"type",self.dns_name.lower(),0):# c.findall(self.dns_name.lower()):
                    #print "Match: %s CISCO: %s" % (c,self.dns_name.lower())
                    return 'cisco'
            for j in self.common_juniper_int:
                if self.extract_tag(j,"type",self.dns_name.lower(),0):# j.findall(self.dns_name.lower()):
                    #print "Match: %s JUNIPER: %s" % (j,self.dns_name.lower())
                    return 'juniper'
            #print "Unknown: %s" % (self.dns_name.lower())
            return 'unknown'

    def parse_for_conn(self):
        #if(self.ip.return_s1() in self.dns_name):
            #This is probably a dhcp client
        #    return 'client'
        #else:
            # for loops can be simplified using python sytatic
            # sugar!!!
        for c in self.common_core_int:
            if self.extract_tag(c,"function",self.dns_name.lower(),0):# c.findall(self.dns_name.lower()):
                return 'core'
        for j in self.common_peering_int:
            if  self.extract_tag(j,"function",self.dns_name.lower(),0):#j.findall(self.dns_name.lower()):
                return 'peering'
        for d in self.common_access_int:
            if  self.extract_tag(d,"function",self.dns_name.lower(),0):#d.findall(self.dns_name.lower()):
                return 'access'
        return 'unknown'
      
    def city_search(self, city_trie):
        name = self.dns_name
        for i in range(len(name)):
            for j in range(0,31):
                if i+j>len(name):
                    break
                to_test = self.unique_name[i:i+j]
                try:
                    #to_test = self.unique_name[i:i+j]
                    city_trie[to_test.lower()]
                    #print "HIT: %s" %(to_test) 
                    #Add tag!!!
                    self.add_tag("geo", to_test, i,i+j)
                except trie.NeedMore:
                    #print "NM: %s" %(to_test) 
                    continue
                except KeyError:
                    #print "KE: %s" %(to_test)
                    continue
                    #Not break
                except:
                    print "Trie threw an unknown error"

    def ip_search(self):
        #print "IP: %s" %(self.dns_name)
        for i in self.link_ip:
            #print "search"
            if self.extract_tag(i, "unique_ip", self.dns_name,0):
                #print "found ip tag"
                return 'ip'

#Feature 1: Number of dotted fields
#Feature 2: All caps and '-'
#Feature 3: #fields >0 in left most
#Feature 4: #fields >1 in left most
#Feature 5: Struct 1 appears in slot 1
#Feature 6: Geo appears in first slot
#Feature 7: Media type tag appears in first slot
#Feature 8: Media position tag appears in first slot
#Feature 9: Function tag appears in first slot
#Feature 10: Function tag appears in second slot
    def create_feature_vector(self):
        name = self.dns_name.lower()
        fv = []
        f1 = name.split('.')
        #Feature 1
        fv.append(len(f1)) #Number of features
        #Cut off the provider ID
        if len(f1) < 4:
            return ''
        #f1.pop()
        #f1.pop()
#        for i in f1:
        #Feature 2
        i = f1[0]
        #Need to work out extract relative vs. exact pos
        #this will actually work left to right
        #Should be changed !!!
        if  self.extract_tag(feature_2,"f2",i,0):#feature_2.findall(i):
            fv.append(1)
        else:
            fv.append(0)
        # Leftmost features
           #fv.append(len(i)) # #letters
        j = i.split('-')
            #fv.append(len(j)-1) # of hyphens
            #Add as ark object to check for tags
        #Feature 3
        if len(j)-1 > 0:
            fv.append(1)
        else:
            fv.append(0)
        #Feature 4
        if len(j)-1 > 1:
            fv.append(1)
        else:
            fv.append(0)
        #Feature 5
        if  self.extract_tag(feature_5,"f5",i,0):#feature_5.findall(i):
            fv.append(1)
        else:
            fv.append(0)
        #Feature 6
        #Blank for now

        #ark = ArkDNSEntry()
        #ark.add_timestamp(0)
        #ark.add_ip('0.0.0.0')
        #ark.add_dns_name(i.lower())
        #[JPC]changes feature from leftmost to
        #entire match
        #ark.add_dns_name(name)

        if len(f1)>1:
            i2 = f1[1]
        else:
            i2 = 'unknown' #[JPC] stupid short-term hack
#        ark2 = ArkDNSEntry()
#        ark2.add_timestamp(0)
#        ark2.add_ip('0.0.0.0')
#        ark2.add_dns_name(i2.lower())
        #Feature 7
        val1 = self.parse_for_int()
        val2 = self.parse_for_speed()
        if val1!='unknown' or val2 != 'unknown':
            fv.append(5)
        else:
            fv.append(0)
        #Feature 8
        if feature_8.findall(i):
            fv.append(1)
        else:
            fv.append(0)
        #Feature 9
        if self.parse_for_conn()=='unknown': # device position known
            fv.append(0)
        else:
            fv.append(1)
        #Feature 10
#        if ark2.parse_for_conn()=='unknown': # device position known
#            fv.append(0)
#        else:
#            fv.append(1)        

        return fv
    


re.I #Case insensitive

#This is a driver function for the pathaudit.py script. The structure of this
#script needs some serious cleaning
def tags5_analysis(dns_names):
    #setup dictionaries
    city_dict_io = open('dictionary.dat', 'r')
    city_trie = trie.Trie()
    for cities in city_dict_io:
        tmp = cities.rstrip().lower()
        if len(tmp)>3:
            city_trie[tmp] = 0
    #print "Calculating and sorting feature vectors"
    for i in dns_names:
        if len(i)<3:
            continue
        if i[0] =='*':
            print i
            continue
        to_proc = ArkDNSEntry()
        to_proc.add_dns_name(i.lower())
        fv = to_proc.create_feature_vector()
        to_proc.city_search(city_trie)
        to_proc.ip_search()
        #to_proc.remove_overlap()
        #if fv != '': 
#        if lev3.findall(i[::-1]) or rr.findall(i[::-1]) or cog.findall(i[::-1]) or tf.findall(i[::-1]):
        #print i
        #for j in fv:
        #    print str(j),
        #    print ",",
        #print "\n",
        to_proc.print_tags5_console()

#Tags5 can be run directly, "bulk tagging mode"

def option0():
# Step one: Read in cycle_dns_file
# add to dictionary for fast lookup
    f = open(sys.argv[2],'r')
    
    dns_to_ip = {}
    total_hops = 0
    name_coverage = 0

    print "Initializing DNS library"
    for lines in f:
        strs = lines.split('\t')
        t_ip = strs[1].rstrip().lower()
        t_dns = strs[2].rstrip().lower()
        if ("non-authoritative" not in t_dns) and ("timeout" not in t_dns) and ("in-addr.arpa" not in t_dns) and ("server-failure" not in t_dns):
            dns_to_ip[t_ip] = t_dns
#Step two: Parse paths
#Keep as little in memory as possible
#Eat a path
#Count the tags
#Assign tags
#Data parse
    print "Processing paths"
    g = open(sys.argv[3],'r')
    reg_hop = re.compile('\d+[.]\d+[.]\d+[.]\d+[,]\d+')
    zz = 0
    dns_names = []

    path_coverage_cdf = open('path_coverage_cdf.dat', 'w')
    restart_file = open('restart.txt','w')
    line_report = open('line_report.txt','w')
    for line in g:
        linecount = 0
        total_line_entries = 0
        total_lines = 0
        strs = line.split('\t')
        report_line_entries = []
        for entries in strs:
            if reg_hop.findall(entries):
                e2 = entries.split(',') #Strip off tailing comma 
            #all_hops.append(e2[0])
            #for itr in resolved:
                total_hops = total_hops+1
                total_line_entries = total_line_entries+1
                if e2[0] in dns_to_ip:  
                    #print "IP: %s, DNS: %s" %(e2[0],dns_to_ip[e2[0]])
                    linecount +=1 
                    name_coverage +=1
                    #dns_names.append(dns_to_ip[e2[0]].lower()[::-1])
                    #restart_file.write(dns_to_ip[e2[0]].lower()[::-1])
                    restart_file.write(dns_to_ip[e2[0]].lower())
                    restart_file.write("\n")
                    report_line_entries.append(total_line_entries)
        zz+=1
        if zz > 100000:
            print "*"
            zz = 0
        path_coverage_cdf.write(str(linecount))
        path_coverage_cdf.write("\t")
        path_coverage_cdf.write(str(total_line_entries))
        path_coverage_cdf.write("\t")
        line_report.write(str(report_line_entries))
        line_report.write("$")
        line_report.write(str(total_line_entries))
        line_report.write("\n")
        if linecount == 0:
             path_coverage_cdf.write("0")
        else:
            path_coverage_cdf.write(str(float(linecount)/float(total_line_entries)))
        path_coverage_cdf.write("\n")    

    print "There are %d dns names on record" %(len(dns_to_ip))  
    print "Total network hops: %d" %(total_hops)
    print "Total resoved hops: %d" %(name_coverage)
    
    path_coverage_cdf.close()
    restart_file.close()
    line_report.close()

def option1():
    print "Reading restart file"
    dns_names = []
    restart_file = open('restart_uniq.txt','r')
    for lines in restart_file:
        dns_names.append(lines.rstrip())

    titlefile = open('titles5.txt','w')
    outfile = open('outfile5.txt', 'w')
    tagfile = open('tagfile5.txt', 'w')

#Read in dictionary
    print "Reading dictionaries"
    city_dict_io = open('dictionary.dat', 'r')
    city_trie = trie.Trie()
    for cities in city_dict_io:
        tmp = cities.rstrip().lower()
        if len(tmp)>3:
            city_trie[tmp] = 0

#pprint(list(city_trie.iteritems()))
    print "Calculating and sorting feature vectors"
    for i in dns_names:
        to_proc = ArkDNSEntry()
        to_proc.add_dns_name(i)
        fv = to_proc.create_feature_vector()
        to_proc.city_search(city_trie)
        to_proc.ip_search()
        if fv != '': 
            titlefile.write(i)
            titlefile.write("\n")
            for j in fv:
                outfile.write(str(j))
                outfile.write(",")
            outfile.write("\n")
            to_proc.print_tags(tagfile)

#d.print_stats()
    titlefile.close()
    outfile.close()
    tagfile.close()

def option2():
    all_tags = tag_bundle()
    tagfile = open('tagfile5.txt','r')
    #Read in tag file to array
    for lines in tagfile:
        t = j_tag()
        l = lines.rstrip()
        ln_val = l.split('\t')
        t.name = ln_val[0]
        t.tag_name = ln_val[1]
        t.tag_value = ln_val[2]
        t.start = int(ln_val[3])
        t.end = int(ln_val[4])
        all_tags.add_tag(t)
    #Remove overlap?
#    print "There are %d tags" %(len(all_tags.tb))
    print "Remove overlap"
    tag_p.jtype = tag_p.speed
    all_tags.remove_overlap()
    print "Total tags: %d\n" %(all_tags.total_tags())
    all_tags.tags_per_name()
    all_tags.print_tag_per_name_dis()
    all_tags.tags_per_type()
    all_tags.print_type_name_dis()
    all_tags.print_top_tag_values()
    by_domain = all_tags.tags_per_naming_domain()
    print "There are %d naming domains" %(len(by_domain))
    all_tags.gen_one_off()
    #[JPC] remeber to analyze the new_tagfile
    new_tags = open('new_tagfile5.txt','w')
    for rem_tags in all_tags.tb:
        new_tags.write(rem_tags.name+'\t'+rem_tags.get_whole_tag())
    new_tags.close()

#---

re.I #Case insensitive regexp
#If this "module" is run as a standalone script
if __name__ == "__main__":
    if sys.argv[1]=='0':
        option0()
    elif sys.argv[1]=='1':
        option1()
    else:
        option2()
